#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

from common import add_common_args, find_matching_image, iter_files, setup_logging, yolo_bbox_from_xyxy


RDD_CLASSES_MULTI = ["D00", "D10", "D20", "D40"]


def get_size(root, image_path):
    size = root.find("size")
    if size is not None and size.findtext("width") and size.findtext("height"):
        return int(float(size.findtext("width"))), int(float(size.findtext("height")))
    if image_path:
        with Image.open(image_path) as im:
            return im.size
    raise ValueError("Cannot determine image size")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert RDD VOC XML to YOLO, mapping D40 to pothole.")
    add_common_args(parser)
    parser.add_argument("--xml-dir", required=True, type=Path)
    parser.add_argument("--image-dir", action="append", type=Path, default=[])
    parser.add_argument("--out-label-dir", required=True, type=Path)
    parser.add_argument("--mode", choices=["pothole_only", "multiclass"], default="pothole_only")
    args = parser.parse_args()
    setup_logging(args.verbose)

    class_to_id = {"D40": 0} if args.mode == "pothole_only" else {c: i for i, c in enumerate(RDD_CLASSES_MULTI)}
    image_dirs = args.image_dir or [args.xml_dir]
    args.out_label_dir.mkdir(parents=True, exist_ok=True)
    converted = kept = skipped = 0
    for xml_path in iter_files(args.xml_dir, {".xml"}):
        try:
            root = ET.parse(xml_path).getroot()
            image_path = find_matching_image(xml_path.stem, image_dirs)
            width, height = get_size(root, image_path)
            lines = []
            for obj in root.findall("object"):
                name = (obj.findtext("name") or "").strip()
                if name not in class_to_id:
                    skipped += 1
                    continue
                box = obj.find("bndbox")
                if box is None:
                    skipped += 1
                    continue
                vals = [float(box.findtext(k)) for k in ("xmin", "ymin", "xmax", "ymax")]
                x, y, w, h = yolo_bbox_from_xyxy(*vals, width, height)
                if w <= 0 or h <= 0:
                    skipped += 1
                    continue
                lines.append(f"{class_to_id[name]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
                kept += 1
            (args.out_label_dir / f"{xml_path.stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
            converted += 1
        except Exception as exc:
            logging.error("Failed to convert %s: %s", xml_path, exc)
    logging.info("Converted %d XML files; kept %d objects; skipped %d objects.", converted, kept, skipped)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
