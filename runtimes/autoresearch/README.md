# AutoResearch isolated runtime

This directory contains the Linux executor and private grader used by AutoResearch. It does not contain model weights, task answers, a root filesystem or prebuilt native binaries. **Its portable build/install sequence has not yet been executed on a fresh Linux host.**

## Requirements

- Dedicated Linux x86-64 host with root access, namespaces, mount/chroot and writable cgroup-v1 CPU/memory/process controllers.
- GCC 11.4.0 targeting `x86_64-linux-gnu`, Linux headers and standard build tools.
- Python 3 with `jsonschema` for host-side checks; the isolated task Python 3.10 comes from the pinned image.
- Image `swebench/swesmith.x86_64.project-monai_1776_monai.a09c1f08@sha256:ada19e0d27dadb991c5b6112e00f116b26359067d5298650eb2eeff7d8385af2`, materialized under `/var/lib/camg/oci-rootfs/` using the provided image helper.
- Prepared AutoResearch data, including the reference task `air-passengers-forecast-dataset@1` used for real execution and grading probes.

## Build, install, then test isolation

Run on the dedicated Linux host, not a workstation with unrelated data. Copy this directory to a build directory outside the Git checkout so generated files do not change the source tree:

```bash
cp -a runtimes/autoresearch /srv/camg/autoresearch-build
cd /srv/camg/autoresearch-build
bash build_bundle.sh
sudo bash install_bundle.sh
sudo env CAMG_AUTORESEARCH_PROBE_DATA=/srv/camg/data/autoresearch \
  bash /tmp/camg-autoresearch/source/verify_installation.sh
```

`build_bundle.sh` performs two independent native builds, compares their bytes, writes actual build provenance and an inventory of every required file, then runs protocol tests. Expected component hashes are read from this content-verified inventory, not inherited from binaries built on another host. It does **not** claim that isolation works.

`install_bundle.sh` installs the verified inventory at `/tmp/camg-autoresearch/source`, checks ownership and permissions, and removes stale installation-test status. These paths currently form one runtime instance per host. Do not install a second instance over a running one.

`verify_installation.sh` performs real namespace/resource, public execution, private grading, failure and cleanup checks. Successful evidence is bound to the runtime contents and the current host boot. It then records installation approval. If a probe fails, investigate its saved evidence; never create approval files manually or disable isolation to proceed.

The reference task is read from the same prepared `train.json`, `grader.json`, public-task directory and private-grader directory used by the service. The test runs a fixed baseline on this task; it is an installation check, not an evaluation result or training-data subset.

## Runtime boundaries

The agent executes in a bounded public workspace. Private grading receives the submission separately. The runtime preserves network isolation, privilege dropping, process/memory/CPU limits and explicit workspace lifecycle operations. A metadata request is not proof that these properties have been exercised.

Persistent task data and final experiment outputs should live outside `/tmp`. The temporary runtime can be reinstalled after reboot, but it must pass the installation checks again. Before reinstalling or cleaning it, stop its client/service and verify there are no active owned processes or mounts. `remote_cleanup.sh --remove-idle-installation` refuses a busy runtime; it is never called automatically by training.
