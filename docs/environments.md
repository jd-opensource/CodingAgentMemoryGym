# Set up the task environments

The commands below describe the intended Linux setup. **A clean-machine deployment of this source package has not yet been executed.** See [verification status](verification.md) for the checks completed so far and the remaining work. Prepare one environment at a time before starting a full training job.

## 1. Choose a dedicated Linux host

Use an isolated Linux x86-64 machine. Coding and AutoResearch need privileged namespace/mount operations and writable cgroup-v1 CPU, memory and process controllers. General and Visual need Docker. These are execution environments for model-generated code: do not install them on a machine containing unrelated credentials or user data.

Keep services and training clients on the same host. The supplied addresses are `127.0.0.1`; no public listener or cross-host port forwarding is needed. Root privileges are for the isolated service host, not for ordinary code inspection.

Storage needs include the source datasets, repository mirrors, container images, unpacked image filesystems, model weights, checkpoints and concurrent episode workspaces. The AutoResearch image alone has about 30.5 GB of unpacked regular-file content. Measure the complete image and dataset selection before scheduling concurrent work; the repository size is not a useful estimate of runtime storage.

Create a separate Python 3.12 environment for services:

```bash
python3.12 -m venv /srv/camg/service-venv
source /srv/camg/service-venv/bin/activate
python -m pip install -r requirements-environments.txt
python -m pip install -e . --no-deps
```

Dependency installation is still a candidate recipe, not an already-verified lock for a fresh machine. Shop additionally requires its original Java/search dependencies, described below. Do not install an arbitrary new training-framework version over the bundled source.

## 2. Prepare tasks and their dependencies

First follow [data preparation](data.md). Use `/srv/camg/data` below, or update `deployment.local.json` consistently.

### Shop

Obtain the pinned MemoryArena checkout and original WebShop catalog/search files using the publishers' instructions. The expected MemoryArena commit is `6cd9de14b71915e39ac742a20dc33785e14b6aab`. Install the checkout's native Python dependencies and Java 11; the backend expects a Conda-style Java environment with the JVM library at `JAVA_HOME/lib/jvm/lib/server/libjvm.so` and the executable under `JAVA_HOME/bin`. Check this directory layout rather than passing an arbitrary JDK directory.

The product files and complete Lucene index must match the recorded selection. Rebuild and verify `product_pool.json` using `python -m camg.prepare_shop` as described in [data preparation](data.md#shop). The server refuses a different product-pool hash. Do not replace the original search tool with title matching or another approximate search implementation.

### Coding

1. Prepare the selected task rows using `python -m camg.prepare --environment coding`.
2. Clone [SWE-smith](https://github.com/SWE-bench/SWE-smith) and check out commit `9b74ac08118a85c39c356802f7961893af73e07f`. Install its grading dependencies, including `swebench==4.1.0`.
3. Obtain the task repository mirrors. Each dataset row's `repo` identifies the original GitHub repository. The mirror directory is the last path component of that repository, and its task branch must be named exactly by `instance_id`. Missing or conflicting branch identities are rejected. The service never substitutes a repository's current default branch for a task branch.
4. Materialize the image digests listed in `camg/data/coding/images.json` with `scripts/prepare_images.py`:

```bash
python scripts/prepare_images.py \
  --cache-root /var/lib/camg/oci-rootfs \
  --crane /usr/local/bin/crane \
  --output /srv/camg/data/coding/materialized-images.json
```

Install the original [crane](https://github.com/google/go-containerregistry/tree/main/cmd/crane) image utility first. The helper uses Docker Hub by default, verifies content digests, and calls the included OCI filesystem materializer. This is a large, separate download step; it is never performed implicitly when a training episode starts. Existing verified cached images can be reused.

The small `third_party/swebench_shim/` package extends the installed SWE-bench package path. It does not contain an alternative grader.

### AutoResearch

The task packages, public workspaces and private answers have separate paths. The agent must never receive the private grader directory as a workspace or container mount.

Follow the [isolated-runtime instructions](../runtimes/autoresearch/README.md) to build, install and test the runtime. It uses the Project MONAI image already listed in the Coding image manifest. A source build is not sufficient: the real isolation probes must pass before execution is admitted. The public service will not fall back to unsandboxed execution.

The runtime currently uses fixed, documented paths and cgroup-v1 semantics. Porting it to cgroup-v2 or another operating system is additional work; do not bypass its checks to make startup succeed.

### General and Visual

Install the bundled MiMo runtime dependencies:

```bash
python -m pip install -e third_party/mimo_runtime/mimoagent
```

Use the official [MiMo dataset and container instructions](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss). Prepare General's task folders and both selected Parquet tables with the data-preparation commands. A working Docker daemon and the task images are required; table conversion does not check containers or task verifiers.

`mimo.agent_environment` in `deployment.local.json` identifies the separate Python environment mounted into task containers for their agent/tool bridge. It needs the original MiMo MCP/agent dependencies. The exact portable installation of this container-side environment and historical image digests remains a deployment-verification item; the current image tags alone do not establish historical equivalence.

General and Visual use model-based judging where specified by their native tasks. Provide the intended judge explicitly in the service process environment:

```bash
export GA_JUDGE_URL='https://your-approved-model-provider.example/v1'
export GA_JUDGE_MODEL='your-general-judge-model'
read -r -s -p 'General judge API key: ' GA_JUDGE_KEY; echo
export GA_JUDGE_KEY

export WD_JUDGE_URL='https://your-approved-model-provider.example/v1'
export WD_JUDGE_MODEL='your-visual-judge-model'
read -r -s -p 'Visual judge API key: ' WD_JUDGE_KEY; echo
export WD_JUDGE_KEY
```

Run those commands in Bash. The URLs are placeholders. Use a provider authorized to receive the relevant task content, and record the actual judge model/version for comparisons. No default endpoint or credential is included. Credentials are not written into generated configuration files.

## 3. Bind the configuration to your installation

```bash
cp deployment.example.json deployment.local.json
# Edit the absolute paths in deployment.local.json for your installation.
python -m camg.configure --deployment deployment.local.json --output prepared
```

Run this from a clean Git checkout after committing any source changes. It records the actual public source commit, hashes the installed files and writes five service configurations, `routes.json`, and a schedule with the matching configuration hash. It preserves task IDs, task order and sampling settings. The generated configuration is **not** a certificate that the services have run successfully.

An absent executable, runtime lock or prepared manifest is an error, not an invitation to insert a placeholder hash. Configuration output belongs outside version control; `prepared/` and `deployment.local.json` are ignored.

## 4. Start the services in separate foreground terminals

```bash
python -m camg.serve --config prepared/shop.json
python -m camg.serve --config prepared/coding.json
python -m camg.serve --config prepared/autoresearch.json
python -m camg.serve --config prepared/general.json
python -m camg.serve --config prepared/visual.json
```

Each command is a separate long-running process. AutoResearch starts its private grader as a supervised child, uses a fresh local credential, and stops the task service if the grader exits. Other task services own their episode managers. On normal shutdown, the service closes its active episodes. Abrupt process or host termination still requires checking owned containers, mounts and workspaces before reuse.

Use `--check-config` to check the configuration without starting a service. This does not validate the assets, sandbox, Docker, judge or task behavior. General/Visual checks also require their judge variables.

The configured ports are:

| Shop | Coding | AutoResearch | General | Visual |
|---|---|---|---|---|
| 65131 | 65134 | 65133 | 65139 | 65140 |

Inspect the corresponding loopback `/metadata` response and service logs. Before training, test a complete reset → action → task termination → cleanup path in each environment. Check the task identity, native reward, context reset and file persistence. For Visual, also check a real screenshot and judge response. These target-runtime tests have not yet been performed for this source package.

## 5. Stop and retain evidence

Stop training clients first, then stop their environment services with Ctrl-C. Keep trajectories, outcome records and logs in the run directory. Check that each service's owned containers, processes and temporary mounts have exited; do not remove other processes or shared assets to clear a failed run. A new AutoResearch invocation requires a fresh service-state directory until the previous service has been checked and cleaned.
