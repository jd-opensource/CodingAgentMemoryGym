# Prepare CAMG-II data

The [CAMG-II dataset on Hugging Face](https://huggingface.co/datasets/LiruiLuo/CAMG-II) collects the five environments' task definitions, training schedule, and supporting files. Use a separate data directory, for example `/srv/camg/data`.

```bash
python -m pip install -e '.[data]'
python -m camg.download --output /srv/camg/CAMG-II
```

For one environment, add `--environment coding`, `autoresearch`, `general`, `visual`, or `shop`. The downloader checks the release's file sizes and checksums. The preparation commands below download only the files they need, so a full download is optional.

The full bundle is approximately 13.3 GB. Shop's 7.2 GB catalog is a separate download from its original publisher. Review the [source-specific terms](../camg/data/LICENSES.md) before use.

## 1. Coding

```bash
python -m camg.prepare --environment coding --download \
  --output /srv/camg/data/coding
```

This downloads the pinned SWE-smith Parquet files from CAMG-II, converts their 11 shards into canonical JSONL, checks their recorded hashes, and checks the exact order of the **3,768 selected task IDs**. If the full bundle is already downloaded, replace `--download` with `--source /srv/camg/CAMG-II/assets/coding`.

Dataset revision: `ea6d7173829c7ec8fa16c22055699ff2e9188091`. SWE-smith code revision: `9b74ac08118a85c39c356802f7961893af73e07f`.

Obtain the corresponding [official SWE-smith assets](https://swesmith.com/getting_started/assets/), including mirrors containing each selected instance branch. The environment resolves mirrors by the last component of the record's `repo` field. `camg/data/coding/images.json` supplies 110 pinned image digests; `scripts/prepare_oci_rootfs.py --help` describes the digest-checked root-filesystem builder. It requires Linux, root privileges and `crane`; see [environment setup](environments.md).

## 2. AutoResearch

The selection contains **762 training tasks / 664 source families** and **169 held-out tasks / 140 families**. The two sets share neither task IDs nor source families.

```bash
python -m camg.prepare --environment autoresearch --download \
  --accept-upstream-terms --output /srv/camg/data/autoresearch
```

CAMG-II includes **651 ready-made archives**, copied unchanged from the pinned OpenMLE release. The remaining **280 tasks use upstream reconstruction recipes**. The command prepares the available archives and lists the tasks to reconstruct in `preparation.json`. To use an existing full download, replace `--download` with `--source /srv/camg/CAMG-II/assets/autoresearch/archives`.

For missing tasks:

1. Read that task's source URLs and terms in `camg/data/autoresearch/acquisition.json`.
2. Download the pinned reconstruction tools:

   ```bash
   hf download FrontisAI/OpenMLE-Tasks build_task.py task_index.jsonl requirements.txt \
     --repo-type dataset --revision f56e4b31252a9b81d95fea100098cd49b7290398 \
     --local-dir /srv/camg/openmle-rebuild
   ```
3. Follow the [publisher's reconstruction instructions](https://huggingface.co/datasets/FrontisAI/OpenMLE-Tasks/blob/f56e4b31252a9b81d95fea100098cd49b7290398/README.md), using the recorded `task_key`. Some sources require you to sign in to Kaggle and accept the dataset terms there.
4. Place archives with the recorded checksums in a directory as `<task_id>.tar.zst`, and rerun with `--source /path/to/archives`. If reconstruction produces a different checksum, inspect the source version and build output before retrying.

Every materialized public file, metric implementation and private answer must match its recorded checksum. Public and private files are put in separate directories. The task service exposes only the public view. Do not mount the preparation directory, task archive or private-grader directory inside the agent's workspace.

To try preparation with a single task, add `--task-id amazon-echo-dot-2-reviews-dataset@1`.

## 3. General

```bash
python -m camg.prepare --environment general --download \
  --output /srv/camg/data/general
```

The included 925 task rows preserve the selected order and prompts. The training schedule uses 797 of these task indices; the remaining 128 are not referenced by that schedule. The command downloads their task assets from CAMG-II and replaces only the machine-local `env_task_dir` path. It writes `tasks.parquet` and a checksum record. Existing assets can be supplied as `--source /srv/camg/CAMG-II/assets/general/envs`.

The original asset source is recorded in `general/source.json`; `camg/data/hub.json` pins the CAMG-II download release.

## 4. Visual

```bash
python -m camg.prepare --environment visual \
  --output /srv/camg/data/visual
```

This converts the included 500 selected rows into the service's Parquet format without changing task order or prompts. Download the referenced official MiMo web-development image separately. Configure screenshot rendering and the visual judge as described in [environment setup](environments.md#general-and-visual).

## 5. Shop

Shop tasks are generated from a verified product selection using the original MemoryArena/WebShop search and purchase behavior.

1. Obtain a clean [MemoryArena](https://github.com/ZexueHe/MemoryArena) checkout at `6cd9de14b71915e39ac742a20dc33785e14b6aab`.
2. Download the [publisher's product catalog and native search assets](https://huggingface.co/datasets/ai-hyz/MemoryArena-product-db), respecting their terms:

   ```bash
   python -m camg.download --environment shop --include-shop-catalog \
     --output /srv/camg/CAMG-II
   ```

   The command downloads and verifies `items_shuffle.json`, `items_ins_v2.json`, and `search_engine/indexes-full/` under `/srv/camg/CAMG-II/assets/shop/catalog`.
3. Install the native Java 11 / search / spaCy dependencies documented by MemoryArena. The backend expects the conda-style Java layout `<java-home>/lib/jvm/lib/server/libjvm.so`; verify your installation layout rather than guessing the path.
4. Rebuild the selected product pool:

```bash
PYTHONPATH="$PWD" python -m camg.prepare_shop \
  --memoryarena-root /srv/camg/upstream/MemoryArena \
  --items-file /srv/camg/CAMG-II/assets/shop/catalog/items_shuffle.json \
  --attributes-file /srv/camg/CAMG-II/assets/shop/catalog/items_ins_v2.json \
  --search-root /srv/camg/CAMG-II/assets/shop/catalog/search_engine \
  --java-home /srv/camg/java11 --output /srv/camg/data/shop
```

The command checks the full search-index inventory and requires the regenerated product pool to match the selected pool's checksum. Obtain catalog assets from the original publisher under its terms, then keep the generated pool in your local data directory.

The training recipe uses 6,400 procedural tasks, generator and price seed 233, a reseeded training stream starting at orbit 0, and zero dedicated note-writing rewards. Do not replace native search with a title-only index.

## Data licenses

See [dataset terms and changes](../camg/data/LICENSES.md) and [third-party notices](../THIRD_PARTY.md). OpenMLE materials include noncommercial and source-specific terms; this repository's software license does not override them.
