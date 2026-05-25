#!/usr/bin/env python3
import argparse
import logging
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

from common import add_common_args, count_files, load_datasets, project_root, resolve_path, setup_logging, write_json


def stream_download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with out_path.open("wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc=out_path.name) as bar:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk)
                bar.update(len(chunk))


def extract_if_zip(path: Path, out_dir: Path) -> bool:
    if path.suffix.lower() != ".zip":
        return False
    logging.info("Extracting %s", path)
    with zipfile.ZipFile(path) as zf:
        zf.extractall(out_dir)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Download datasets from Zenodo records declared in configs/datasets.yaml.")
    add_common_args(parser)
    parser.add_argument("--dataset", help="Optional dataset name to download.")
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--keep-archive", action="store_true", help="Keep downloaded archive after extraction.")
    args = parser.parse_args()
    setup_logging(args.verbose)

    rows = []
    for ds in load_datasets(args.config):
        if ds.get("source_type") != "zenodo":
            continue
        if args.dataset and ds["name"] != args.dataset:
            continue
        raw_dir = resolve_path(ds["raw_dir"])
        raw_dir.mkdir(parents=True, exist_ok=True)
        existing = count_files(raw_dir)["total_files"]
        if existing and not args.force:
            logging.info("%s already has files; skipping. Use --force to download again.", ds["name"])
            status = "downloaded_existing"
        else:
            record = ds.get("zenodo_record")
            if not record:
                logging.error("%s has no zenodo_record.", ds["name"])
                status = "failed"
            else:
                api_url = f"https://zenodo.org/api/records/{record}"
                try:
                    data = requests.get(api_url, timeout=60).json()
                    files = data.get("files", [])
                    if not files:
                        raise RuntimeError("No files found in Zenodo record.")
                    downloaded = []
                    for item in files:
                        key = item["key"]
                        url = item["links"]["self"]
                        out_path = raw_dir / key
                        if out_path.exists() and not args.force:
                            logging.info("Archive exists: %s", out_path)
                        else:
                            stream_download(url, out_path)
                        downloaded.append(str(out_path))
                        if extract_if_zip(out_path, raw_dir) and not args.keep_archive:
                            out_path.unlink()
                    status = "downloaded"
                    write_json({"name": ds["name"], "zenodo_record": record, "files": files, "downloaded": downloaded}, raw_dir / "download_manifest.json")
                except Exception as exc:
                    logging.error("Zenodo download failed for %s: %s", ds["name"], exc)
                    status = "failed"
        row = {"name": ds["name"], "status": status, "raw_dir": ds["raw_dir"], "stats": count_files(raw_dir)}
        rows.append(row)

    write_json(rows, project_root() / "docs" / "zenodo_download_manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
