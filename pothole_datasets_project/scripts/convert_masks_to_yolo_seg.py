#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path

import cv2
import numpy as np

from common import add_common_args, iter_files, setup_logging


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert binary/class masks to YOLO segmentation polygons.")
    add_common_args(parser)
    parser.add_argument("--mask-dir", required=True, type=Path)
    parser.add_argument("--out-label-dir", required=True, type=Path)
    parser.add_argument("--class-id", type=int, default=0)
    parser.add_argument("--mask-value", type=int, default=None, help="Specific pixel value to keep. Default: all non-zero pixels.")
    parser.add_argument("--min-area", type=float, default=30.0)
    parser.add_argument("--epsilon-ratio", type=float, default=0.002, help="Polygon simplification ratio relative to contour perimeter.")
    args = parser.parse_args()
    setup_logging(args.verbose)
    args.out_label_dir.mkdir(parents=True, exist_ok=True)

    converted = polygons = skipped = 0
    for mask_path in iter_files(args.mask_dir, {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}):
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            logging.warning("Cannot read mask: %s", mask_path)
            skipped += 1
            continue
        binary = (mask == args.mask_value).astype(np.uint8) if args.mask_value is not None else (mask > 0).astype(np.uint8)
        h, w = binary.shape[:2]
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lines = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < args.min_area:
                skipped += 1
                continue
            eps = args.epsilon_ratio * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, eps, True).reshape(-1, 2)
            if len(approx) < 3:
                skipped += 1
                continue
            coords = []
            for x, y in approx:
                coords.extend([f"{x / w:.6f}", f"{y / h:.6f}"])
            lines.append(f"{args.class_id} " + " ".join(coords))
            polygons += 1
        (args.out_label_dir / f"{mask_path.stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        converted += 1
    logging.info("Converted %d masks; wrote %d polygons; skipped %d contours.", converted, polygons, skipped)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
