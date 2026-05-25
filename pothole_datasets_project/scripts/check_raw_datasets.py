#!/usr/bin/env python3
import argparse
from pathlib import Path

from common import add_common_args, count_files, load_datasets, project_root, resolve_path, setup_logging, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Check raw dataset folders and write download status.")
    add_common_args(parser)
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    args = parser.parse_args()
    setup_logging(args.verbose)

    lines = ["# Download Status", "", "| Dataset | Status | Source | Raw path | File summary |", "|---|---|---|---|---|"]
    rows = []
    for ds in load_datasets(args.config):
        raw_dir = resolve_path(ds["raw_dir"])
        stats = count_files(raw_dir)
        if stats["total_files"] > 0:
            status = "downloaded"
        elif ds.get("status") == "manual_download_required" or ds.get("source_type") == "manual":
            status = "manual_required"
        else:
            status = "not_downloaded"
        summary = ", ".join(f"{k}={v}" for k, v in stats.items())
        lines.append(f"| {ds['name']} | {status} | {ds.get('source', '')} | `{ds['raw_dir']}` | {summary} |")
        rows.append({"name": ds["name"], "status": status, "source": ds.get("source"), "raw_dir": ds["raw_dir"], "stats": stats})

    docs = project_root() / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "download_status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_json(rows, docs / "raw_dataset_check.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
