def attest_public(value, expected_runtime_digest, expected_limits):
    required_true = (
        "formal_eligible",
        "network_namespace",
        "network_no_egress",
        "dns_disabled",
        "metadata_service_blocked",
        "external_unix_sockets_blocked",
        "pid_namespace",
        "ipc_namespace",
        "mount_namespace",
        "workspace_quota",
        "tmpfs_limit",
        "file_size_limit",
        "open_files_limit",
        "fresh_unprivileged_uid_gid",
        "capabilities_dropped",
        "no_new_privs",
        "seccomp",
        "read_only_rootfs",
        "workspace_noexec",
        "instrumented_python_only",
        "isolated_proc",
        "minimal_devices",
        "gpu_devices_absent",
        "core_dumps_disabled",
        "mount_denied",
        "ptrace_denied",
        "setuid_denied",
        "user_namespace_creation_denied",
        "ebpf_denied",
        "raw_sockets_denied",
        "kernel_module_denied",
        "container_engine_absent",
        "background_process_detection",
        "descendant_kill_reap",
        "parent_death_cleanup_watchdog",
        "freeze_reap",
        "read_only_workspace_freeze",
        "teardown_cgroup_empty",
        "teardown_mount_empty",
        "idempotent_teardown",
        "cumulative_managed_runtime_budget",
    )
    if value.get("contract") != "openmle_fast_linux_cgroup_namespace_runner_v1":
        raise ValueError("public contract mismatch")
    if value.get("runtime_digest") != expected_runtime_digest:
        raise ValueError("public runtime mismatch")
    if value.get("resource_limits") != expected_limits:
        raise ValueError("public limits mismatch")
    _attest_versioned_cgroups(value)
    if any(value.get(name) is not True for name in required_true):
        raise ValueError("public boolean attestation incomplete")
    if value.get("execution_counter_coverage") != "complete":
        raise ValueError("public execution accounting incomplete")
    if value.get("fit_counter_coverage") != "partial":
        raise ValueError("public fit coverage drift")
    if not value.get("active_verification", {}).get("admission_stamp_valid"):
        raise ValueError("public active admission missing")
    return True

def attest_private(value, expected_runtime_digest, expected_limits):
    required_true = (
        "formal_eligible",
        "fresh_worker_per_grade",
        "selected_task_only_mounts",
        "submission_passed_by_fd",
        "all_task_inputs_passed_by_fd",
        "result_sanitized_ipc",
        "service_environment_hidden",
        "network_namespace",
        "network_no_egress",
        "dns_disabled",
        "metadata_service_blocked",
        "external_unix_sockets_blocked",
        "pid_namespace",
        "ipc_namespace",
        "mount_namespace",
        "fresh_unprivileged_uid_gid",
        "capabilities_dropped",
        "no_new_privs",
        "seccomp",
        "read_only_rootfs",
        "isolated_proc",
        "minimal_devices",
        "gpu_devices_absent",
        "core_dumps_disabled",
        "hard_wall_supervision",
        "descendant_kill_reap",
        "parent_death_cleanup_watchdog",
        "worker_teardown_verified",
        "validate_submission_once",
        "evaluate_once_after_validation",
    )
    if value.get("contract") != "openmle_fast_private_grader_runner_v1":
        raise ValueError("private contract mismatch")
    if value.get("runtime_digest") != expected_runtime_digest:
        raise ValueError("private runtime mismatch")
    if value.get("resource_limits") != expected_limits:
        raise ValueError("private limits mismatch")
    _attest_versioned_cgroups(value)
    if any(value.get(name) is not True for name in required_true):
        raise ValueError("private boolean attestation incomplete")
    if not value.get("active_verification", {}).get("admission_stamp_valid"):
        raise ValueError("private active admission missing")
    return True

def _attest_versioned_cgroups(value):
    version = value.get("cgroup_version")
    if version not in ("v1", "hybrid", "v2"):
        raise ValueError("unsupported cgroup version")
    prefix = "cgroup_v1_" if version in ("v1", "hybrid") else "cgroup_v2_"
    if any(value.get(prefix + name) is not True for name in ("cpu", "memory", "pids")):
        raise ValueError("selected cgroup controller set incomplete")
    if version in ("v1", "hybrid") and any(
        value.get("cgroup_v2_" + name) is not False for name in ("cpu", "memory", "pids")
    ):
        raise ValueError("cgroup-v2 coverage was fabricated")
    attestation = value.get("cgroup_controller_attestation")
    if not isinstance(attestation, dict) or attestation.get("version") != version:
        raise ValueError("controller attestation version mismatch")
