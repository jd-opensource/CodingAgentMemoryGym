#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define REAL_PYTHON_FD 198
#define FIT_EVENT_FD 199
#define REAL_PYTHON_PATH "/run/openmle-bin/openmle-real-python"
#define FIT_EVENT_PATH "/run/openmle-hook/fit-events"

extern char **environ;

static const char *BOOTSTRAP =
    "import importlib.util as _u;"
    "_s=_u.spec_from_file_location('_openmle_fit_hook','/run/openmle-hook/fit_hook.py');"
    "_m=_u.module_from_spec(_s);_s.loader.exec_module(_m);_m.bootstrap()";

static void fail(const char *message) {
    dprintf(STDERR_FILENO, "managed Python launcher failure: %s: %s\n",
            message, strerror(errno));
    _exit(126);
}

static void verify_fd_identity(int target, const char *path, int flags,
                               mode_t expected_type, int expected_access,
                               int require_nonblock) {
    int target_flags = fcntl(target, F_GETFL);
    if (target_flags < 0) {
        if (errno != EBADF) fail("inspect instrumentation fd");
        int source = open(path, flags);
        if (source < 0) fail("open instrumentation endpoint");
        if (source != target) {
            if (dup2(source, target) < 0) fail("install instrumentation fd");
            close(source);
        }
        target_flags = fcntl(target, F_GETFL);
        if (target_flags < 0) fail("inspect installed instrumentation fd");
    }
    int reference = open(path, flags);
    if (reference < 0) fail("open instrumentation reference");
    struct stat target_stat, reference_stat;
    if (fstat(target, &target_stat) != 0 ||
        fstat(reference, &reference_stat) != 0)
        fail("stat instrumentation fd");
    if (target_stat.st_dev != reference_stat.st_dev ||
        target_stat.st_ino != reference_stat.st_ino)
        fail("instrumentation fd identity mismatch");
    if ((expected_type == S_IFREG && !S_ISREG(target_stat.st_mode)) ||
        (expected_type == S_IFIFO && !S_ISFIFO(target_stat.st_mode)))
        fail("instrumentation fd type mismatch");
    if ((target_flags & O_ACCMODE) != expected_access)
        fail("instrumentation fd access mismatch");
    if (require_nonblock && !(target_flags & O_NONBLOCK))
        fail("instrumentation fd blocking mode mismatch");
    close(reference);
    if (fcntl(target, F_SETFD, 0) != 0)
        fail("make instrumentation fd inheritable");
}

static int simple_option(const char *value) {
    const char *options[] = {
        "-u", "-B", "-E", "-s", "-S", "-O", "-OO", "-q",
    };
    for (size_t i = 0; i < sizeof(options) / sizeof(options[0]); i++) {
        if (strcmp(value, options[i]) == 0) return 1;
    }
    return 0;
}

static int prohibited_module(const char *value) {
    const char *names[] = {"pip", "ensurepip", "venv"};
    for (size_t i = 0; i < sizeof(names) / sizeof(names[0]); i++) {
        size_t size = strlen(names[i]);
        if (strcmp(value, names[i]) == 0 ||
            (strncmp(value, names[i], size) == 0 && value[size] == '.'))
            return 1;
    }
    return 0;
}

static int workspace_script(const char *value) {
    char resolved[PATH_MAX];
    if (!realpath(value, resolved)) return 0;
    return strncmp(resolved, "/workspace/", strlen("/workspace/")) == 0;
}

int main(int argc, char **argv) {
    verify_fd_identity(REAL_PYTHON_FD, REAL_PYTHON_PATH,
                       O_RDONLY | O_CLOEXEC, S_IFREG, O_RDONLY, 0);
    verify_fd_identity(FIT_EVENT_FD, FIT_EVENT_PATH,
                       O_WRONLY | O_NONBLOCK | O_CLOEXEC,
                       S_IFIFO, O_WRONLY, 1);

    int cursor = 1;
    while (cursor < argc && simple_option(argv[cursor])) cursor++;

    if (cursor < argc &&
        (strcmp(argv[cursor], "-V") == 0 ||
         strcmp(argv[cursor], "--version") == 0)) {
        char *version_argv[] = {"python", "-I", argv[cursor], NULL};
        fexecve(REAL_PYTHON_FD, version_argv, environ);
        fail("execute version query");
    }

    const char *mode = "stdin";
    int payload = cursor;
    if (cursor < argc && strcmp(argv[cursor], "-c") == 0) {
        mode = "command";
        payload = cursor + 1;
        if (payload >= argc) {
            errno = EINVAL;
            fail("missing -c command");
        }
    } else if (cursor < argc && strcmp(argv[cursor], "-m") == 0) {
        mode = "module";
        payload = cursor + 1;
        if (payload >= argc) {
            errno = EINVAL;
            fail("missing -m module");
        }
        if (prohibited_module(argv[payload])) {
            errno = EPERM;
            fail("prohibited Python module");
        }
    } else if (cursor < argc && strcmp(argv[cursor], "-") != 0) {
        mode = "script";
        payload = cursor;
        if (!workspace_script(argv[payload])) {
            errno = EPERM;
            fail("script outside workspace");
        }
    } else if (cursor < argc && strcmp(argv[cursor], "-") == 0) {
        payload = cursor + 1;
    }

    if (setenv("OPENMLE_PYTHON_MODE", mode, 1) != 0)
        fail("set launcher mode");

    size_t extra = (size_t)(argc - payload);
    char **managed = calloc(extra + 6, sizeof(char *));
    if (!managed) fail("allocate argv");
    size_t out = 0;
    managed[out++] = "python";
    managed[out++] = "-I";
    managed[out++] = "-B";
    managed[out++] = "-c";
    managed[out++] = (char *)BOOTSTRAP;
    for (int i = payload; i < argc; i++) managed[out++] = argv[i];
    managed[out] = NULL;

    fexecve(REAL_PYTHON_FD, managed, environ);
    fail("execute pinned Python");
    return 126;
}
