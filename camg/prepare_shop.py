"""Rebuild the Shop product selection from the original catalog and native search."""
from __future__ import annotations
import argparse
from pathlib import Path
from .prepare import DATA, sha256, write_json

EXPECTED_POOL = "7ca77d3f9f2a0007eed54a17aa6f8d275ce8ec200ae47daeca3b70cafdd506c6"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("memoryarena-root", "items-file", "attributes-file", "search-root", "java-home", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    from .services.shop.native_webshop_backend import MemoryArenaNativeWebShopBackend
    from .services.shop.procedural.certifier import certify_native_product_pool
    from .services.shop.procedural.pool_io import write_product_pool_manifest
    from .services.shop.procedural.provenance import verify_lucene_index_manifest
    manifest = DATA / "shop/lucene.sha256"
    # Match the native backend's search-engine directory convention.
    index = args.search_root / "indexes-full"
    verify_lucene_index_manifest(manifest, index_dir=index)
    backend = MemoryArenaNativeWebShopBackend(memoryarena_root=args.memoryarena_root,
        items_file=args.items_file, attributes_file=args.attributes_file, search_root=args.search_root,
        java_home=args.java_home, price_seed=233)
    backend.start()
    pool, evidence = certify_native_product_pool(backend, catalog_sha256=sha256(args.items_file),
        attributes_sha256=sha256(args.attributes_file), lucene_index_sha256=sha256(manifest))
    args.output.mkdir(parents=True, exist_ok=True)
    digest = write_product_pool_manifest(pool, args.output / "product_pool.json")
    write_json(args.output / "selection-check.json", {"expected_sha256": EXPECTED_POOL, "observed_sha256": digest, "matches": digest == EXPECTED_POOL})
    if digest != EXPECTED_POOL:
        raise RuntimeError("Regenerated product selection differs from CAMG-II; do not train with it as the same dataset")
    print("Shop product selection matches the recorded checksum. Task execution has not been tested.")


if __name__ == "__main__":
    main()
