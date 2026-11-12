# Dataset terms and changes

This directory contains the CAMG-II task selection and metadata, not a new blanket license for the underlying data.

- `general/` and `visual/`: selected XiaomiMiMo MiMo-V2.6-RL-oss rows, under its published Apache-2.0 terms. Prompts, task identities and row order are preserved. Local asset paths were replaced by a preparation placeholder; files were serialized as JSONL.
- `autoresearch/`: CAMG task/split manifests and task instructions derived from the pinned OpenMLE release. OpenRSI's original materials use **CC BY-NC 4.0**; underlying datasets retain the individual source terms recorded in each manifest. Instructions are preserved byte-for-byte to keep task identity. Data files, private answers, metric implementations and archives must be obtained from their publishers. See [OpenRSI LICENSE](https://github.com/FrontisAI/OpenRSI/blob/main/LICENSE), [NOTICE](https://github.com/FrontisAI/OpenRSI/blob/main/NOTICE), and each task's `source_urls` and `license_name_or_permission`.
- `coding/`: selection IDs, task ordering and image hashes for the MIT-licensed SWE-smith release. Software repositories, datasets inside images and other dependencies retain their own terms.
- `shop/`: search-index checksums only. Neither the product catalog nor the derived product pool is redistributed. Check the original MemoryArena/product publisher's terms before acquiring them.
- `train_schedule.jsonl`: ordered references into these pools. It does not contain task solutions or replace the source datasets.

Attribution: Xiaomi MiMo Team (MiMo-V2.6-RL-oss); FrontisAI (OpenMLE/OpenRSI); SWE-bench/SWE-smith authors; MemoryArena and WebShop authors. The root repository's software license does not override these data terms.
