#!/usr/bin/env python3
import argparse
import logging
import subprocess
from pathlib import Path

from common import add_common_args, count_files, load_datasets, project_root, resolve_path, setup_logging, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Download Kaggle datasets declared in configs/datasets.yaml.")
    add_common_args(parser)
    parser.add_argument("--dataset", help="Optional dataset name to download.")
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    parser.add_argument("--force", action="store_true", help="Run download even when files already exist.")
    args = parser.parse_args()
    setup_logging(args.verbose)

    rows = []
    for ds in load_datasets(args.config):
        if ds.get("source_type") != "kaggle":
            continue
        if args.dataset and ds["name"] != args.dataset:
            continue
        raw_dir = resolve_path(ds["raw_dir"])
        raw_dir.mkdir(parents=True, exist_ok=True)
        if count_files(raw_dir)["total_files"] and not args.force:
            logging.info("%s already has files; skipping. Use --force to download again.", ds["name"])
            status = "downloaded_existing"
        else:
            cmd = ["kaggle", "datasets", "download", "-d", ds["source"], "-p", str(raw_dir), "--unzip"]
            logging.info("Downloading %s with Kaggle API.", ds["name"])
            try:
                subprocess.run(cmd, check=True)
                status = "downloaded"
            except FileNotFoundError:
                logging.error("kaggle command not found. Install requirements and configure ~/.kaggle/kaggle.json.")
                status = "failed"
            except subprocess.CalledProcessError as exc:
                logging.error("Kaggle download failed for %s: %s", ds["name"], exc)
                status = "failed"
        stats = count_files(raw_dir)
        rows.append({"name": ds["name"], "status": status, "raw_dir": ds["raw_dir"], "stats": stats})
        write_json(rows[-1], raw_dir / "download_manifest.json")

    write_json(rows, project_root() / "docs" / "kaggle_download_manifest.json")
    logging.info("Wrote docs/kaggle_download_manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
