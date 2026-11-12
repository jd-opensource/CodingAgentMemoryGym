# Dataset terms and changes

The CAMG-II task selection and metadata use the following source-specific terms.

- `general/` and `visual/`: selected XiaomiMiMo MiMo-V2.6-RL-oss rows, under its published Apache-2.0 terms. Prompts, task identities and row order are preserved. Local asset paths were replaced by a preparation placeholder; files were serialized as JSONL. The Hugging Face release also includes the original General task assets and readable Parquet task tables.
- `autoresearch/`: CAMG task/split manifests and task instructions derived from the pinned OpenMLE release. OpenRSI's original materials use **CC BY-NC 4.0**; underlying datasets retain the individual source terms recorded in each manifest. Instructions are preserved byte-for-byte. The Hugging Face release mirrors 651 ready-made archives, including their original notices, grading resources, and data. The remaining 280 tasks use upstream reconstruction recipes. See [OpenRSI LICENSE](https://github.com/FrontisAI/OpenRSI/blob/main/LICENSE), [NOTICE](https://github.com/FrontisAI/OpenRSI/blob/main/NOTICE), and each task's `source_urls` and `license_name_or_permission`.
- `coding/`: selection IDs, task ordering and image hashes for the MIT-licensed SWE-smith release. The Hugging Face release includes the selected task records and pinned source Parquet files. Software repositories, datasets inside images and other dependencies retain their own terms.
- `shop/`: procedural task indices, generator settings, source download metadata, and search-index checksums. The catalog download command fetches the original publisher's files under its terms.
- `train_schedule.jsonl`: ordered task references into these pools.

Attribution: Xiaomi MiMo Team (MiMo-V2.6-RL-oss); FrontisAI (OpenMLE/OpenRSI); SWE-bench/SWE-smith authors; MemoryArena and WebShop authors. The root repository's software license does not override these data terms.
