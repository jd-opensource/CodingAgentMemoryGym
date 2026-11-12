#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <grp.h>
#include <linux/audit.h>
#include <linux/capability.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sched.h>
#include <signal.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mount.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/sysmacros.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define MAX_PROCS 256
#define REAL_PYTHON_FD 198
#define FIT_EVENT_FD 199

#ifndef SECCOMP_RET_KILL_PROCESS
#define SECCOMP_RET_KILL_PROCESS SECCOMP_RET_KILL
#endif

#ifndef PTRACE_O_EXITKILL
#define PTRACE_O_EXITKILL (1 << 20)
#endif

struct config {
    const char *rootfs;
    const char *workspace;
    const char *run_dir;
    const char *wrapper;
    const char *fit_hook;
    const char *real_python;
    const char *command;
    int stats_fd;
    int managed_ms;
    rlim_t max_open_files;
    rlim_t max_file_bytes;
};

enum exec_kind {
    EXEC_UNKNOWN = 0,
    EXEC_SHELL = 1,
    EXEC_WRAPPER = 2,
    EXEC_REAL_PYTHON = 3,
    EXEC_UTILITY = 4,
};

struct proc_state {
    pid_t pid;
    int active;
    int managed;
    int io_collected;
    enum exec_kind kind;
    double managed_started;
};

struct trace_stats {
    int exit_code;
    int security_violation;
    int managed_runtime_limit;
    int background_process;
    int file_limit;
    int attempts;
    int completed;
    int nested;
    int fits;
    int active;
    int process_peak;
    unsigned long long bytes_read;
    unsigned long long bytes_written;
    double completed_managed_seconds;
};

static void __attribute__((noreturn)) die(const char *message) {
    int saved = errno;
    dprintf(STDERR_FILENO, "openmle supervisor setup failure: %s: %s\n",
            message, strerror(saved));
    _exit(125);
}

static int mkdir_one(const char *path, mode_t mode) {
    if (mkdir(path, mode) == 0 || errno == EEXIST) {
        return 0;
    }
    return -1;
}

static void path_join(char *out, size_t size, const char *left, const char *right) {
    if (snprintf(out, size, "%s/%s", left, right) >= (int)size) {
        errno = ENAMETOOLONG;
        die("path too long");
    }
}

static void parse_config(int argc, char **argv, struct config *cfg) {
    memset(cfg, 0, sizeof(*cfg));
    cfg->stats_fd = -1;
    for (int i = 1; i < argc; i++) {
        if (i + 1 >= argc) {
            errno = EINVAL;
            die("missing argument value");
        }
        const char *name = argv[i++];
        const char *value = argv[i];
        if (strcmp(name, "--rootfs") == 0) cfg->rootfs = value;
        else if (strcmp(name, "--workspace") == 0) cfg->workspace = value;
        else if (strcmp(name, "--run-dir") == 0) cfg->run_dir = value;
        else if (strcmp(name, "--wrapper") == 0) cfg->wrapper = value;
        else if (strcmp(name, "--fit-hook") == 0) cfg->fit_hook = value;
        else if (strcmp(name, "--real-python") == 0) cfg->real_python = value;
        else if (strcmp(name, "--command") == 0) cfg->command = value;
        else if (strcmp(name, "--stats-fd") == 0) cfg->stats_fd = atoi(value);
        else if (strcmp(name, "--managed-ms") == 0) cfg->managed_ms = atoi(value);
        else if (strcmp(name, "--max-open-files") == 0)
            cfg->max_open_files = (rlim_t)strtoull(value, NULL, 10);
        else if (strcmp(name, "--max-file-bytes") == 0)
            cfg->max_file_bytes = (rlim_t)strtoull(value, NULL, 10);
        else {
            errno = EINVAL;
            die("unknown argument");
        }
    }
    if (!cfg->rootfs || !cfg->workspace || !cfg->run_dir || !cfg->wrapper ||
        !cfg->fit_hook || !cfg->real_python || !cfg->command ||
        cfg->stats_fd < 0 || cfg->managed_ms <= 0 ||
        cfg->max_open_files == 0 || cfg->max_file_bytes == 0) {
        errno = EINVAL;
        die("incomplete arguments");
    }
}

static void bind_read_only_file(const char *source, const char *target) {
    int fd = open(target, O_CREAT | O_WRONLY | O_CLOEXEC, 0500);
    if (fd < 0) die("create bind target");
    close(fd);
    if (mount(source, target, NULL, MS_BIND, NULL) != 0) die("bind file");
    if (mount(NULL, target, NULL,
              MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV,
              NULL) != 0) {
        die("remount bind file read-only");
    }
}

static int open_real_python(const struct config *cfg) {
    char path[4096];
    if (snprintf(path, sizeof(path), "%s%s", cfg->rootfs, cfg->real_python) >=
        (int)sizeof(path)) {
        errno = ENAMETOOLONG;
        die("real Python path");
    }
    int fd = open(path, O_RDONLY | O_CLOEXEC);
    if (fd < 0) die("open real Python");
    return fd;
}

static void setup_mounts(const struct config *cfg, char *merged, size_t merged_size) {
    char store[4096], upper[4096], work[4096], options[12288];
    path_join(store, sizeof(store), cfg->run_dir, "overlay-store");
    if (mkdir_one(store, 0700) != 0) die("mkdir overlay store");
    if (mount("tmpfs", store, "tmpfs", MS_NOSUID | MS_NODEV,
              "size=64m,nr_inodes=8192,mode=0700") != 0) {
        die("mount overlay store");
    }
    path_join(upper, sizeof(upper), store, "upper");
    path_join(work, sizeof(work), store, "work");
    path_join(merged, merged_size, store, "merged");
    if (mkdir_one(upper, 0755) != 0 || mkdir_one(work, 0700) != 0 ||
        mkdir_one(merged, 0755) != 0) {
        die("mkdir overlay directories");
    }
    if (chmod(upper, 0755) != 0 || chmod(merged, 0755) != 0)
        die("chmod overlay traversal directories");
    if (snprintf(options, sizeof(options), "lowerdir=%s,upperdir=%s,workdir=%s",
                 cfg->rootfs, upper, work) >= (int)sizeof(options)) {
        errno = ENAMETOOLONG;
        die("overlay options");
    }
    if (mount("overlay", merged, "overlay", MS_NOSUID | MS_NODEV, options) != 0) {
        die("mount root overlay");
    }

    char workspace[4096], tmp[4096], proc[4096], dev[4096], sysdir[4096], run[4096];
    char oldroot[4096];
    path_join(workspace, sizeof(workspace), merged, "workspace");
    path_join(tmp, sizeof(tmp), merged, "tmp");
    path_join(proc, sizeof(proc), merged, "proc");
    path_join(dev, sizeof(dev), merged, "dev");
    path_join(sysdir, sizeof(sysdir), merged, "sys");
    path_join(run, sizeof(run), merged, "run");
    path_join(oldroot, sizeof(oldroot), merged, ".oldroot");
    if (mkdir_one(oldroot, 0700) != 0) die("mkdir pivot oldroot");
    if (mkdir_one(workspace, 0755) != 0) die("mkdir workspace mountpoint");
    if (mount(cfg->workspace, workspace, NULL, MS_BIND, NULL) != 0)
        die("bind workspace");
    if (mount(NULL, workspace, NULL,
              MS_BIND | MS_REMOUNT | MS_NOEXEC | MS_NOSUID | MS_NODEV,
              NULL) != 0) {
        die("remount workspace noexec");
    }

    if (mount("tmpfs", tmp, "tmpfs", MS_NOEXEC | MS_NOSUID | MS_NODEV,
              "size=268435456,nr_inodes=32768,mode=1777") != 0)
        die("mount private tmp");

    if (mount("tmpfs", dev, "tmpfs", MS_NOEXEC | MS_NOSUID,
              "size=1m,nr_inodes=128,mode=0755") != 0)
        die("mount minimal dev");
    struct {
        const char *name;
        mode_t mode;
        unsigned int major_no;
        unsigned int minor_no;
    } devices[] = {
        {"null", S_IFCHR | 0666, 1, 3},
        {"zero", S_IFCHR | 0666, 1, 5},
        {"random", S_IFCHR | 0666, 1, 8},
        {"urandom", S_IFCHR | 0666, 1, 9},
    };
    for (size_t i = 0; i < sizeof(devices) / sizeof(devices[0]); i++) {
        char node[4096];
        path_join(node, sizeof(node), dev, devices[i].name);
        if (mknod(node, devices[i].mode,
                  makedev(devices[i].major_no, devices[i].minor_no)) != 0)
            die("create minimal device");
        if (chmod(node, devices[i].mode & 07777) != 0)
            die("chmod minimal device");
    }
    char fd_link[4096], stdin_link[4096], stdout_link[4096], stderr_link[4096];
    path_join(fd_link, sizeof(fd_link), dev, "fd");
    path_join(stdin_link, sizeof(stdin_link), dev, "stdin");
    path_join(stdout_link, sizeof(stdout_link), dev, "stdout");
    path_join(stderr_link, sizeof(stderr_link), dev, "stderr");
    if (symlink("/proc/self/fd", fd_link) != 0 ||
        symlink("/proc/self/fd/0", stdin_link) != 0 ||
        symlink("/proc/self/fd/1", stdout_link) != 0 ||
        symlink("/proc/self/fd/2", stderr_link) != 0)
        die("create device fd links");
    if (chmod(dev, 0555) != 0)
        die("lock minimal dev directory");

    if (mount("proc", proc, "proc", MS_NOEXEC | MS_NOSUID | MS_NODEV,
              "hidepid=2") != 0)
        die("mount namespace proc with hidepid");
    if (mount("tmpfs", sysdir, "tmpfs", MS_NOEXEC | MS_NOSUID | MS_NODEV,
              "size=4096,nr_inodes=16,mode=0555") != 0)
        die("mount empty sys");
    if (mount(NULL, sysdir, NULL,
              MS_REMOUNT | MS_RDONLY | MS_NOEXEC | MS_NOSUID | MS_NODEV,
              NULL) != 0)
        die("remount empty sys read-only");

    if (mount("tmpfs", run, "tmpfs", MS_NOSUID | MS_NODEV,
              "size=4m,nr_inodes=256,mode=0755") != 0)
        die("mount private run");
    char bindir[4096], hookdir[4096], wrapper_target[4096], hook_target[4096];
    char fit_fifo[4096], real_python_source[4096], real_python_target[4096];
    path_join(bindir, sizeof(bindir), run, "openmle-bin");
    path_join(hookdir, sizeof(hookdir), run, "openmle-hook");
    if (mkdir_one(bindir, 0555) != 0 || mkdir_one(hookdir, 0555) != 0)
        die("mkdir instrumentation directories");
    /* mkdir modes are filtered by the inherited process umask.  The runner
       can be called concurrently, so make the intended traversal contract
       explicit instead of depending on a process-global ambient setting. */
    if (chmod(bindir, 0555) != 0 || chmod(hookdir, 0555) != 0)
        die("chmod instrumentation directories");
    path_join(wrapper_target, sizeof(wrapper_target), bindir,
              "openmle-python-wrapper");
    path_join(hook_target, sizeof(hook_target), hookdir, "fit_hook.py");
    path_join(fit_fifo, sizeof(fit_fifo), hookdir, "fit-events");
    path_join(real_python_target, sizeof(real_python_target), bindir,
              "openmle-real-python");
    if (snprintf(real_python_source, sizeof(real_python_source), "%s%s",
                 cfg->rootfs, cfg->real_python) >=
        (int)sizeof(real_python_source)) {
        errno = ENAMETOOLONG;
        die("real Python bind source");
    }
    bind_read_only_file(cfg->wrapper, wrapper_target);
    bind_read_only_file(cfg->fit_hook, hook_target);
    bind_read_only_file(real_python_source, real_python_target);
    if (mkfifo(fit_fifo, 0622) != 0 || chmod(fit_fifo, 0622) != 0)
        die("create fit event FIFO");
    const char *names[] = {"python", "python3", "python3.10"};
    for (size_t i = 0; i < sizeof(names) / sizeof(names[0]); i++) {
        char linkpath[4096];
        path_join(linkpath, sizeof(linkpath), bindir, names[i]);
        if (symlink("openmle-python-wrapper", linkpath) != 0)
            die("create managed Python link");
    }
    if (mount(NULL, run, NULL,
              MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV,
              NULL) != 0)
        die("remount private run read-only");

    if (mount(NULL, merged, NULL,
              MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV, NULL) != 0)
        die("remount root overlay read-only");
}

static void enter_sandbox_mount_root(const char *merged) {
    if (chdir(merged) != 0) die("chdir new root");
    if (syscall(SYS_pivot_root, ".", ".oldroot") != 0)
        die("pivot to sandbox root");
    if (chdir("/") != 0) die("chdir sandbox root");
    if (umount2("/.oldroot", MNT_DETACH) != 0) die("detach old root");
}

static void write_all(int fd, const char *value) {
    size_t left = strlen(value);
    while (left > 0) {
        ssize_t written = write(fd, value, left);
        if (written < 0) {
            if (errno == EINTR) continue;
            die("write synchronization pipe");
        }
        value += written;
        left -= (size_t)written;
    }
}

static void write_file(const char *path, const char *value, int optional) {
    int fd = open(path, O_WRONLY | O_CLOEXEC);
    if (fd < 0) {
        if (optional && errno == ENOENT) return;
        die("open namespace map");
    }
    size_t size = strlen(value);
    if (write(fd, value, size) != (ssize_t)size) {
        close(fd);
        die("write namespace map");
    }
    close(fd);
}

static void install_user_map(const char *merged, pid_t child) {
    char path[4096];
    if (snprintf(path, sizeof(path), "%s/proc/%d/setgroups", merged, child) >=
        (int)sizeof(path)) {
        errno = ENAMETOOLONG;
        die("setgroups path");
    }
    write_file(path, "deny\n", 1);
    if (snprintf(path, sizeof(path), "%s/proc/%d/uid_map", merged, child) >=
        (int)sizeof(path)) {
        errno = ENAMETOOLONG;
        die("uid map path");
    }
    write_file(path, "0 0 1\n1000 65534 1\n", 0);
    if (snprintf(path, sizeof(path), "%s/proc/%d/gid_map", merged, child) >=
        (int)sizeof(path)) {
        errno = ENAMETOOLONG;
        die("gid map path");
    }
    write_file(path, "0 0 1\n1000 65534 1\n", 0);
}

#define DENY_SYSCALL(name)                                                    \
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_##name, 0, 1),                  \
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_TRAP)

#define ERRNO_SYSCALL(name, value)                                            \
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_##name, 0, 1),                  \
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | ((value) & SECCOMP_RET_DATA))

static void install_seccomp(void) {
    const uint32_t namespace_flags =
        CLONE_NEWNS | CLONE_NEWCGROUP | CLONE_NEWUTS | CLONE_NEWIPC |
        CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNET;
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 (uint32_t)offsetof(struct seccomp_data, arch)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 (uint32_t)offsetof(struct seccomp_data, nr)),
        DENY_SYSCALL(mount),
        DENY_SYSCALL(umount2),
        DENY_SYSCALL(pivot_root),
        DENY_SYSCALL(ptrace),
        DENY_SYSCALL(unshare),
        DENY_SYSCALL(setns),
        DENY_SYSCALL(bpf),
        DENY_SYSCALL(perf_event_open),
        DENY_SYSCALL(init_module),
        DENY_SYSCALL(finit_module),
        DENY_SYSCALL(delete_module),
        DENY_SYSCALL(kexec_load),
        DENY_SYSCALL(reboot),
        DENY_SYSCALL(swapon),
        DENY_SYSCALL(swapoff),
        DENY_SYSCALL(open_by_handle_at),
        DENY_SYSCALL(name_to_handle_at),
        DENY_SYSCALL(keyctl),
        DENY_SYSCALL(add_key),
        DENY_SYSCALL(request_key),
        ERRNO_SYSCALL(socket, EPERM),
        ERRNO_SYSCALL(socketpair, EPERM),
        DENY_SYSCALL(mknod),
        DENY_SYSCALL(mknodat),
        DENY_SYSCALL(chroot),
        DENY_SYSCALL(setuid),
        DENY_SYSCALL(setgid),
        DENY_SYSCALL(setreuid),
        DENY_SYSCALL(setregid),
        DENY_SYSCALL(setresuid),
        DENY_SYSCALL(setresgid),
        DENY_SYSCALL(setfsuid),
        DENY_SYSCALL(setfsgid),
        DENY_SYSCALL(capset),
        DENY_SYSCALL(seccomp),
        DENY_SYSCALL(memfd_create),
#ifdef __NR_userfaultfd
        DENY_SYSCALL(userfaultfd),
#endif
#ifdef __NR_clone3
        ERRNO_SYSCALL(clone3, ENOSYS),
#endif
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_clone, 0, 5),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 (uint32_t)offsetof(struct seccomp_data, args[0])),
        BPF_STMT(BPF_ALU | BPF_AND | BPF_K, namespace_flags),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_TRAP),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 (uint32_t)offsetof(struct seccomp_data, nr)),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };
    struct sock_fprog program = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0)
        die("set no_new_privs");
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &program) != 0)
        die("install seccomp");
}

static void set_limit(int resource, rlim_t value) {
    struct rlimit limit = {.rlim_cur = value, .rlim_max = value};
    if (setrlimit(resource, &limit) != 0) die("set rlimit");
}

static void drop_capability_bounding_set(void) {
    for (int cap = 0; cap <= 63; cap++) {
        if (prctl(PR_CAPBSET_DROP, cap, 0, 0, 0) != 0 && errno != EINVAL)
            die("drop capability bounding bit");
    }
}

static void clear_capabilities(void) {
    struct __user_cap_header_struct header;
    struct __user_cap_data_struct data[2];
    memset(&header, 0, sizeof(header));
    memset(data, 0, sizeof(data));
    header.version = _LINUX_CAPABILITY_VERSION_3;
    header.pid = 0;
    if (syscall(SYS_capset, &header, data) != 0) die("clear capabilities");
}

static void child_environment(void) {
    if (clearenv() != 0) die("clear environment");
    const char *pairs[][2] = {
        {"PATH", "/run/openmle-bin:/usr/bin:/bin"},
        {"HOME", "/nonexistent"},
        {"TMPDIR", "/tmp"},
        {"TZ", "UTC"},
        {"LC_ALL", "C.UTF-8"},
        {"LANG", "C.UTF-8"},
        {"PYTHONHASHSEED", "0"},
        {"PYTHONDONTWRITEBYTECODE", "1"},
        {"OMP_NUM_THREADS", "1"},
        {"OPENBLAS_NUM_THREADS", "1"},
        {"MKL_NUM_THREADS", "1"},
        {"VECLIB_MAXIMUM_THREADS", "1"},
        {"NUMEXPR_NUM_THREADS", "1"},
        {"CUDA_VISIBLE_DEVICES", ""},
    };
    for (size_t i = 0; i < sizeof(pairs) / sizeof(pairs[0]); i++) {
        if (setenv(pairs[i][0], pairs[i][1], 1) != 0) die("set environment");
    }
}

static void sandbox_child(const struct config *cfg, const char *merged,
                          int real_python_fd, int fit_write,
                          int ready_write, int go_read) {
    (void)merged;
    if (chdir("/workspace") != 0) die("enter sandbox workspace");
    if (setgroups(0, NULL) != 0) die("clear supplementary groups");
    if (unshare(CLONE_NEWUSER) != 0) die("create user namespace");
    write_all(ready_write, "U");
    char ack;
    if (read(go_read, &ack, 1) != 1) die("wait for user map");
    close(ready_write);
    close(go_read);

    if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) != 0) die("ptrace traceme");
    drop_capability_bounding_set();
    if (setresgid(1000, 1000, 1000) != 0) die("drop gid");
    if (setresuid(1000, 1000, 1000) != 0) die("drop uid");
    clear_capabilities();
    if (prctl(PR_SET_KEEPCAPS, 0, 0, 0, 0) != 0) die("clear keepcaps");
    if (prctl(PR_SET_DUMPABLE, 1, 0, 0, 0) != 0) die("set dumpable for tracer");

    set_limit(RLIMIT_FSIZE, cfg->max_file_bytes);
    set_limit(RLIMIT_CORE, 0);
    set_limit(RLIMIT_NPROC, 64);
    if (real_python_fd != REAL_PYTHON_FD) {
        if (dup2(real_python_fd, REAL_PYTHON_FD) < 0)
            die("install real Python fd");
        close(real_python_fd);
    }
    if (fcntl(REAL_PYTHON_FD, F_SETFD, 0) != 0)
        die("make real Python fd inheritable");
    if (fit_write != FIT_EVENT_FD) {
        if (dup2(fit_write, FIT_EVENT_FD) < 0)
            die("install fit event fd");
        close(fit_write);
    }
    if (fcntl(FIT_EVENT_FD, F_SETFD, 0) != 0)
        die("make fit event fd inheritable");
    /* Install reserved instrumentation descriptors before lowering NOFILE.
       Existing descriptors above the soft limit remain valid, while the
       untrusted process cannot allocate new descriptors beyond the cap. */
    set_limit(RLIMIT_NOFILE, cfg->max_open_files);
    close(cfg->stats_fd);
    child_environment();
    install_seccomp();
    if (raise(SIGSTOP) != 0) die("initial ptrace stop");
    execl("/bin/sh", "sh", "-c", cfg->command, (char *)NULL);
    die("exec shell");
}

static double monotonic_seconds(void) {
    struct timespec now;
    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0) die("clock_gettime");
    return (double)now.tv_sec + (double)now.tv_nsec / 1000000000.0;
}

static struct proc_state *find_state(struct proc_state *states, pid_t pid) {
    for (int i = 0; i < MAX_PROCS; i++) {
        if (states[i].active && states[i].pid == pid) return &states[i];
    }
    return NULL;
}

static struct proc_state *add_state(struct proc_state *states, pid_t pid,
                                    struct trace_stats *stats) {
    struct proc_state *existing = find_state(states, pid);
    if (existing) return existing;
    for (int i = 0; i < MAX_PROCS; i++) {
        if (!states[i].active) {
            memset(&states[i], 0, sizeof(states[i]));
            states[i].pid = pid;
            states[i].active = 1;
            stats->active++;
            if (stats->active + 2 > stats->process_peak)
                stats->process_peak = stats->active + 2;
            return &states[i];
        }
    }
    errno = EOVERFLOW;
    die("trace process table exhausted");
}

static int executable_identity(const char *merged, pid_t pid,
                               const struct stat *wrapper_stat,
                               const struct stat *python_stat,
                               char *name, size_t name_size) {
    char path[4096], link[4096];
    if (snprintf(path, sizeof(path), "%s/proc/%d/exe", merged, pid) >=
        (int)sizeof(path))
        return EXEC_UNKNOWN;
    struct stat info;
    if (stat(path, &info) != 0) return EXEC_UNKNOWN;
    if (info.st_dev == wrapper_stat->st_dev && info.st_ino == wrapper_stat->st_ino)
        return EXEC_WRAPPER;
    if (info.st_dev == python_stat->st_dev && info.st_ino == python_stat->st_ino)
        return EXEC_REAL_PYTHON;
    ssize_t size = readlink(path, link, sizeof(link) - 1);
    if (size < 0) return EXEC_UNKNOWN;
    link[size] = '\0';
    const char *base = strrchr(link, '/');
    base = base ? base + 1 : link;
    snprintf(name, name_size, "%s", base);
    return EXEC_UTILITY;
}

// 2026-09-27 blocklist inversion: every utility executes except debuggers,
// tracers, and namespace escape tools. The metered-python invariant
// (EXEC_REAL_PYTHON only as the wrapper's child, checked in handle_exec)
// is unchanged and remains the security spine.
static int blocked_utility(const char *name) {
    const char *blocked[] = {
        "strace", "strace32", "gdb", "gdbserver", "ltrace", "ltrace32",
        "perf", "bpftrace", "nsenter",
    };
    for (size_t i = 0; i < sizeof(blocked) / sizeof(blocked[0]); i++) {
        if (strcmp(name, blocked[i]) == 0) return 1;
    }
    return 0;
}

static void collect_io(const char *merged, struct proc_state *state,
                       struct trace_stats *stats) {
    if (!state || state->io_collected) return;
    char path[4096];
    if (snprintf(path, sizeof(path), "%s/proc/%d/io", merged, state->pid) >=
        (int)sizeof(path))
        return;
    FILE *handle = fopen(path, "r");
    if (!handle) return;
    char key[64];
    unsigned long long value;
    while (fscanf(handle, "%63[^:]: %llu\n", key, &value) == 2) {
        if (strcmp(key, "read_bytes") == 0) stats->bytes_read += value;
        else if (strcmp(key, "write_bytes") == 0) stats->bytes_written += value;
    }
    fclose(handle);
    state->io_collected = 1;
}

static void drain_fit_events(int fd, struct trace_stats *stats) {
    char buffer[4096];
    while (1) {
        ssize_t size = read(fd, buffer, sizeof(buffer));
        if (size <= 0) {
            if (size < 0 && (errno == EINTR)) continue;
            break;
        }
        for (ssize_t i = 0; i < size; i++) {
            if (buffer[i] == 'F') stats->fits++;
        }
    }
}

static double total_managed_seconds(struct proc_state *states,
                                    struct trace_stats *stats,
                                    double now) {
    double total = stats->completed_managed_seconds;
    for (int i = 0; i < MAX_PROCS; i++) {
        if (states[i].active && states[i].managed)
            total += now - states[i].managed_started;
    }
    return total;
}

static void kill_tracees(struct proc_state *states) {
    kill(-1, SIGKILL);
    for (int i = 0; i < MAX_PROCS; i++) {
        if (states[i].active)
            ptrace(PTRACE_CONT, states[i].pid, NULL,
                   (void *)(long)SIGKILL);
    }
}

static void handle_exec(const char *merged, pid_t pid, pid_t main_pid,
                        int *initial_shell_seen, struct proc_state *states,
                        struct trace_stats *stats,
                        const struct stat *wrapper_stat,
                        const struct stat *python_stat) {
    struct proc_state *state = find_state(states, pid);
    if (!state) state = add_state(states, pid, stats);
    char name[256] = "";
    int identity = executable_identity(merged, pid, wrapper_stat, python_stat,
                                       name, sizeof(name));
    if (!*initial_shell_seen && pid == main_pid) {
        *initial_shell_seen = 1;
        state->kind = EXEC_SHELL;
        return;
    }
    if (identity == EXEC_WRAPPER) {
        if (state->managed) {
            stats->security_violation = 1;
            return;
        }
        state->managed = 1;
        state->managed_started = monotonic_seconds();
        state->kind = EXEC_WRAPPER;
        stats->attempts++;
        stats->nested++;
        return;
    }
    if (identity == EXEC_REAL_PYTHON) {
        if (!state->managed || state->kind != EXEC_WRAPPER) {
            stats->security_violation = 1;
            return;
        }
        state->kind = EXEC_REAL_PYTHON;
        return;
    }
    stats->nested++;
    state->kind = EXEC_UTILITY;
    if (identity == EXEC_UNKNOWN || blocked_utility(name))
        stats->security_violation = 1;
}

static void write_stats(const struct config *cfg, const struct trace_stats *stats,
                        double managed_seconds) {
    dprintf(cfg->stats_fd,
            "{\"schema\":\"openmle_fast_supervisor_stats_v1\","
            "\"exit_code\":%d,\"security_violation\":%s,"
            "\"managed_runtime_limit\":%s,\"background_process\":%s,"
            "\"file_limit\":%s,\"execution_attempt_delta\":%d,"
            "\"execution_completed_delta\":%d,"
            "\"nested_subprocess_delta\":%d,\"fit_delta\":%d,"
            "\"process_peak\":%d,\"bytes_read\":%llu,"
            "\"bytes_written\":%llu,"
            "\"managed_runtime_wall_seconds\":%.9f}",
            stats->exit_code,
            stats->security_violation ? "true" : "false",
            stats->managed_runtime_limit ? "true" : "false",
            stats->background_process ? "true" : "false",
            stats->file_limit ? "true" : "false",
            stats->attempts, stats->completed, stats->nested, stats->fits,
            stats->process_peak, stats->bytes_read, stats->bytes_written,
            managed_seconds);
}

static void trace_sandbox(const struct config *cfg, const char *merged,
                          pid_t child, int fit_read,
                          const struct stat *wrapper_stat,
                          const struct stat *python_stat) {
    struct proc_state states[MAX_PROCS];
    struct trace_stats stats;
    memset(states, 0, sizeof(states));
    memset(&stats, 0, sizeof(stats));
    stats.exit_code = 125;
    add_state(states, child, &stats);

    int status;
    if (waitpid(child, &status, 0) != child || !WIFSTOPPED(status))
        die("wait initial ptrace stop");
    long options = PTRACE_O_TRACEEXEC | PTRACE_O_TRACEFORK |
                   PTRACE_O_TRACEVFORK | PTRACE_O_TRACECLONE |
                   PTRACE_O_TRACEEXIT | PTRACE_O_EXITKILL;
    if (ptrace(PTRACE_SETOPTIONS, child, NULL, (void *)options) != 0)
        die("set ptrace options");
    if (ptrace(PTRACE_CONT, child, NULL, NULL) != 0) die("continue trace child");

    int initial_shell_seen = 0;
    int main_exited = 0;
    while (stats.active > 0) {
        drain_fit_events(fit_read, &stats);
        pid_t pid = waitpid(-1, &status, __WALL | WNOHANG);
        if (pid == 0) {
            double managed = total_managed_seconds(states, &stats,
                                                   monotonic_seconds());
            if (!stats.managed_runtime_limit &&
                managed * 1000.0 >= (double)cfg->managed_ms) {
                stats.managed_runtime_limit = 1;
                kill_tracees(states);
            }
            struct timespec pause = {.tv_sec = 0, .tv_nsec = 5000000};
            nanosleep(&pause, NULL);
            continue;
        }
        if (pid < 0) {
            if (errno == EINTR) continue;
            if (errno == ECHILD) break;
            die("wait traced process");
        }
        struct proc_state *state = find_state(states, pid);
        if (!state) state = add_state(states, pid, &stats);

        if (WIFEXITED(status) || WIFSIGNALED(status)) {
            collect_io(merged, state, &stats);
            double now = monotonic_seconds();
            if (state->managed) {
                stats.completed_managed_seconds += now - state->managed_started;
                if (WIFEXITED(status) && WEXITSTATUS(status) == 0 &&
                    !stats.security_violation && !stats.managed_runtime_limit)
                    stats.completed++;
            }
            if (WIFSIGNALED(status) && WTERMSIG(status) == SIGSYS)
                stats.security_violation = 1;
            if (WIFSIGNALED(status) && WTERMSIG(status) == SIGXFSZ)
                stats.file_limit = 1;
            state->active = 0;
            stats.active--;
            if (pid == child) {
                main_exited = 1;
                stats.exit_code = WIFEXITED(status)
                    ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
                if (stats.active > 0 && !stats.security_violation &&
                    !stats.managed_runtime_limit) {
                    stats.background_process = 1;
                    kill_tracees(states);
                }
            }
            continue;
        }

        if (!WIFSTOPPED(status)) continue;
        int sig = WSTOPSIG(status);
        unsigned int event = (unsigned int)status >> 16;
        if (sig == SIGSYS) {
            stats.security_violation = 1;
            kill_tracees(states);
            continue;
        }
        if (event == PTRACE_EVENT_EXEC) {
            handle_exec(merged, pid, child, &initial_shell_seen, states, &stats,
                        wrapper_stat, python_stat);
        } else if (event == PTRACE_EVENT_FORK ||
                   event == PTRACE_EVENT_VFORK ||
                   event == PTRACE_EVENT_CLONE) {
            unsigned long new_pid = 0;
            if (ptrace(PTRACE_GETEVENTMSG, pid, NULL, &new_pid) == 0)
                add_state(states, (pid_t)new_pid, &stats);
        } else if (event == PTRACE_EVENT_EXIT) {
            collect_io(merged, state, &stats);
        }
        if (stats.security_violation) {
            kill_tracees(states);
            continue;
        }
        int deliver = (sig == SIGTRAP || sig == SIGSTOP) ? 0 : sig;
        if (ptrace(PTRACE_CONT, pid, NULL, (void *)(long)deliver) != 0 &&
            errno != ESRCH)
            die("continue traced process");
    }
    if (!main_exited && stats.exit_code == 125) stats.exit_code = 137;
    drain_fit_events(fit_read, &stats);
    double managed = stats.completed_managed_seconds;
    write_stats(cfg, &stats, managed);
}

int main(int argc, char **argv) {
    struct config cfg;
    parse_config(argc, argv, &cfg);
    if (mount(NULL, "/", NULL, MS_REC | MS_PRIVATE, NULL) != 0)
        die("make mounts private");

    int real_python_fd = open_real_python(&cfg);
    char merged[4096];
    setup_mounts(&cfg, merged, sizeof(merged));

    struct stat wrapper_stat, python_stat;
    if (stat(cfg.wrapper, &wrapper_stat) != 0 ||
        fstat(real_python_fd, &python_stat) != 0)
        die("stat managed executables");
    enter_sandbox_mount_root(merged);
    snprintf(merged, sizeof(merged), "/");

    int ready_pipe[2], go_pipe[2];
    int fit_read = open("/run/openmle-hook/fit-events",
                        O_RDONLY | O_NONBLOCK | O_CLOEXEC);
    int fit_write = open("/run/openmle-hook/fit-events",
                         O_WRONLY | O_NONBLOCK | O_CLOEXEC);
    if (fit_read < 0 || fit_write < 0 || pipe2(ready_pipe, O_CLOEXEC) != 0 ||
        pipe2(go_pipe, O_CLOEXEC) != 0)
        die("create supervisor pipes");
    if (fcntl(cfg.stats_fd, F_SETFD, FD_CLOEXEC) != 0)
        die("protect stats fd");

    pid_t child = fork();
    if (child < 0) die("fork sandbox child");
    if (child == 0) {
        close(fit_read);
        close(ready_pipe[0]);
        close(go_pipe[1]);
        sandbox_child(&cfg, merged, real_python_fd, fit_write,
                      ready_pipe[1], go_pipe[0]);
    }
    close(ready_pipe[1]);
    close(go_pipe[0]);
    close(real_python_fd);
    close(fit_write);

    char ready;
    if (read(ready_pipe[0], &ready, 1) != 1) die("await user namespace");
    install_user_map(merged, child);
    write_all(go_pipe[1], "G");
    close(ready_pipe[0]);
    close(go_pipe[1]);

    trace_sandbox(&cfg, merged, child, fit_read, &wrapper_stat, &python_stat);
    close(fit_read);
    close(cfg.stats_fd);
    return 0;
}
