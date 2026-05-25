#!/usr/bin/env python3
import argparse
import logging
from collections import defaultdict
from pathlib import Path

from common import add_common_args, build_alias_map, project_root, setup_logging, yolo_bbox_from_xyxy


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert COCO bbox annotations to YOLO detection labels.")
    add_common_args(parser)
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--out-label-dir", required=True, type=Path)
    parser.add_argument("--classes", nargs="+", default=["pothole"])
    parser.add_argument("--class-mapping", type=Path, default=project_root() / "configs" / "class_mapping.yaml")
    parser.add_argument("--keep-empty", action="store_true", help="Write empty label files for images with no kept boxes.")
    args = parser.parse_args()
    setup_logging(args.verbose)

    try:
        from pycocotools.coco import COCO
    except ImportError:
        logging.error("pycocotools is required. Install requirements.txt.")
        return 2

    coco = COCO(str(args.json))
    alias_map = build_alias_map(args.class_mapping)
    class_to_id = {c: i for i, c in enumerate(args.classes)}
    cat_to_class = {}
    for cid, cat in coco.cats.items():
        raw = str(cat.get("name", ""))
        canonical = alias_map.get(raw.lower().replace("-", "_"), raw)
        if canonical in class_to_id:
            cat_to_class[cid] = canonical

    grouped = defaultdict(list)
    skipped = 0
    for ann in coco.dataset.get("annotations", []):
        canonical = cat_to_class.get(ann.get("category_id"))
        if not canonical or "bbox" not in ann:
            skipped += 1
            continue
        img = coco.imgs[ann["image_id"]]
        x, y, w, h = ann["bbox"]
        bx = yolo_bbox_from_xyxy(x, y, x + w, y + h, img["width"], img["height"])
        if bx[2] <= 0 or bx[3] <= 0:
            skipped += 1
            continue
        grouped[ann["image_id"]].append(f"{class_to_id[canonical]} {bx[0]:.6f} {bx[1]:.6f} {bx[2]:.6f} {bx[3]:.6f}")

    args.out_label_dir.mkdir(parents=True, exist_ok=True)
    image_ids = coco.imgs.keys() if args.keep_empty else grouped.keys()
    for img_id in image_ids:
        stem = Path(coco.imgs[img_id]["file_name"]).stem
        lines = grouped.get(img_id, [])
        (args.out_label_dir / f"{stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    logging.info("Wrote %d label files; skipped %d annotations.", len(list(image_ids)), skipped)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
