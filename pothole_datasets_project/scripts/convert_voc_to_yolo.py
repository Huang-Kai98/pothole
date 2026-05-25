#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

from common import add_common_args, build_alias_map, find_matching_image, iter_files, project_root, setup_logging, yolo_bbox_from_xyxy


def parse_size(root, image_path):
    size = root.find("size")
    if size is not None and size.findtext("width") and size.findtext("height"):
        return int(float(size.findtext("width"))), int(float(size.findtext("height")))
    if image_path and image_path.exists():
        with Image.open(image_path) as im:
            return im.size
    raise ValueError("Cannot determine image size")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Pascal VOC XML boxes to YOLO detection labels.")
    add_common_args(parser)
    parser.add_argument("--xml-dir", required=True, type=Path)
    parser.add_argument("--image-dir", action="append", type=Path, default=[])
    parser.add_argument("--out-label-dir", required=True, type=Path)
    parser.add_argument("--classes", nargs="+", default=["pothole"], help="Canonical class order.")
    parser.add_argument("--class-mapping", type=Path, default=project_root() / "configs" / "class_mapping.yaml")
    parser.add_argument("--skip-unknown", action="store_true", help="Skip classes not in --classes.")
    args = parser.parse_args()
    setup_logging(args.verbose)

    alias_map = build_alias_map(args.class_mapping)
    class_to_id = {c: i for i, c in enumerate(args.classes)}
    args.out_label_dir.mkdir(parents=True, exist_ok=True)
    image_dirs = args.image_dir or [args.xml_dir]
    converted = skipped = 0

    for xml_path in iter_files(args.xml_dir, {".xml"}):
        try:
            root = ET.parse(xml_path).getroot()
            image_path = find_matching_image(xml_path.stem, image_dirs)
            width, height = parse_size(root, image_path)
            lines = []
            for obj in root.findall("object"):
                raw_name = (obj.findtext("name") or "").strip()
                canonical = alias_map.get(raw_name.lower().replace("-", "_"), raw_name)
                if canonical not in class_to_id:
                    if args.skip_unknown:
                        skipped += 1
                        continue
                    logging.warning("Unknown class %s in %s; skipping.", raw_name, xml_path)
                    skipped += 1
                    continue
                box = obj.find("bndbox")
                if box is None:
                    continue
                vals = [float(box.findtext(k)) for k in ("xmin", "ymin", "xmax", "ymax")]
                x, y, w, h = yolo_bbox_from_xyxy(*vals, width, height)
                if w <= 0 or h <= 0:
                    skipped += 1
                    continue
                lines.append(f"{class_to_id[canonical]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
            (args.out_label_dir / f"{xml_path.stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
            converted += 1
        except Exception as exc:
            logging.error("Failed to convert %s: %s", xml_path, exc)
    logging.info("Converted %d XML files; skipped %d objects.", converted, skipped)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
