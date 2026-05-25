#!/usr/bin/env python3
import argparse
from pathlib import Path

from common import add_common_args, count_files, load_datasets, project_root, resolve_path, setup_logging


def card_text(ds):
    stats = count_files(resolve_path(ds["raw_dir"]))
    scale = ", ".join(f"{k}: {v}" for k, v in stats.items())
    return f"""# {ds['name']}
## Source
{ds.get('source', 'TBD')}

## Download
Status: `{ds.get('status', 'unknown')}`

Command: `{ds.get('download_command') or 'manual_download_required'}`

Expected raw path: `{ds.get('raw_dir')}`

## Task Type
{ds.get('task_type', 'TBD')}

## Annotation Format
{ds.get('annotation_format', 'TBD')}

## Classes
{', '.join(map(str, ds.get('classes', [])))}

## Scale
Current local scan: {scale}

## Scene Characteristics
{ds.get('scene_characteristics', 'TBD')}

## Recommended Usage
{ds.get('recommended_usage', 'TBD')}

## Limitations
{ds.get('limitations', 'TBD')}

## License / Usage Restriction
{ds.get('license', 'TBD')}

## Citation
{ds.get('citation', 'TBD')}

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate dataset cards from configs/datasets.yaml.")
    add_common_args(parser)
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    parser.add_argument("--out-dir", type=Path, default=project_root() / "docs" / "dataset_cards")
    args = parser.parse_args()
    setup_logging(args.verbose)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for ds in load_datasets(args.config):
        (args.out_dir / f"{ds['name']}.md").write_text(card_text(ds), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
