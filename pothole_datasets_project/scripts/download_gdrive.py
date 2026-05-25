#!/usr/bin/env python3
import argparse
import logging
import subprocess
from pathlib import Path

from common import add_common_args, count_files, load_datasets, project_root, resolve_path, setup_logging, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Download Google Drive datasets declared in configs/datasets.yaml.")
    add_common_args(parser)
    parser.add_argument("--dataset", help="Optional dataset name to download.")
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    setup_logging(args.verbose)

    rows = []
    for ds in load_datasets(args.config):
        if ds.get("source_type") != "gdrive":
            continue
        if args.dataset and ds["name"] != args.dataset:
            continue
        raw_dir = resolve_path(ds["raw_dir"])
        raw_dir.mkdir(parents=True, exist_ok=True)
        out_path = raw_dir / f"{ds['name']}_download"
        if count_files(raw_dir)["total_files"] and not args.force:
            status = "downloaded_existing"
            logging.info("%s already has files; skipping.", ds["name"])
        else:
            file_id = ds.get("gdrive_id")
            if not file_id:
                logging.error("%s has no gdrive_id.", ds["name"])
                status = "failed"
            else:
                # gdown v6 accepts either a full URL or a file id as the
                # positional argument. Older examples used --id, which is no
                # longer accepted by current releases.
                cmd = ["gdown", file_id, "-O", str(out_path)]
                try:
                    subprocess.run(cmd, check=True)
                    status = "downloaded"
                except FileNotFoundError:
                    logging.error("gdown command not found. Install requirements.txt first.")
                    status = "failed"
                except subprocess.CalledProcessError as exc:
                    logging.error("gdown failed for %s: %s", ds["name"], exc)
                    status = "failed"
        row = {"name": ds["name"], "status": status, "raw_dir": ds["raw_dir"], "stats": count_files(raw_dir)}
        rows.append(row)
        write_json(row, raw_dir / "download_manifest.json")

    write_json(rows, project_root() / "docs" / "gdrive_download_manifest.json")
    logging.info("Wrote docs/gdrive_download_manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
