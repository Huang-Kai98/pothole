#!/usr/bin/env python3
import argparse
import logging
import subprocess
from pathlib import Path

from common import add_common_args, count_files, load_datasets, project_root, resolve_path, setup_logging, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Clone GitHub datasets declared in configs/datasets.yaml.")
    add_common_args(parser)
    parser.add_argument("--dataset", help="Optional dataset name to clone.")
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    args = parser.parse_args()
    setup_logging(args.verbose)

    rows = []
    for ds in load_datasets(args.config):
        if ds.get("source_type") != "github":
            continue
        if args.dataset and ds["name"] != args.dataset:
            continue
        raw_dir = resolve_path(ds["raw_dir"])
        if raw_dir.exists() and count_files(raw_dir)["total_files"]:
            status = "downloaded_existing"
            logging.info("%s already exists; skipping clone.", ds["name"])
        else:
            raw_dir.parent.mkdir(parents=True, exist_ok=True)
            cmd = ["git", "clone", ds["source"], str(raw_dir)]
            try:
                subprocess.run(cmd, check=True)
                status = "downloaded"
            except subprocess.CalledProcessError as exc:
                logging.error("git clone failed for %s: %s", ds["name"], exc)
                status = "failed"
        row = {"name": ds["name"], "status": status, "raw_dir": ds["raw_dir"], "stats": count_files(raw_dir)}
        rows.append(row)
        write_json(row, raw_dir / "download_manifest.json")
    write_json(rows, project_root() / "docs" / "github_download_manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
