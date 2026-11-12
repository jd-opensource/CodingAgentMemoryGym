"""Download CAMG-II task definitions and supporting files from Hugging Face."""
from __future__ import annotations

import argparse
from pathlib import Path

from camg.hub import ENVIRONMENTS, download_dataset, download_shop_catalog


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--environment", choices=(*ENVIRONMENTS, "all"), default="all")
    parser.add_argument("--include-shop-catalog", action="store_true",
        help="Also download the 7.2 GB Shop catalog and search index from the original publisher")
    args = parser.parse_args(argv)
    if args.include_shop_catalog and args.environment not in ("all", "shop"):
        parser.error("--include-shop-catalog requires --environment shop or all")
    root = download_dataset(args.output, args.environment)
    if args.include_shop_catalog:
        download_shop_catalog(root / "assets/shop/catalog")
    print(f"CAMG-II data downloaded and verified: {root}")


if __name__ == "__main__":
    main()
