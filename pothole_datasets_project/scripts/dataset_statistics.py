#!/usr/bin/env python3
import argparse
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

from common import IMAGE_EXTS, add_common_args, count_files, iter_files, load_datasets, project_root, resolve_path, setup_logging


def yolo_label_stats(label_root: Path):
    class_counts = Counter()
    annotated_images = 0
    negative_images = 0
    total_objects = 0
    for txt in iter_files(label_root, {".txt"}):
        lines = [ln.strip() for ln in txt.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
        if lines:
            annotated_images += 1
        else:
            negative_images += 1
        for ln in lines:
            parts = ln.split()
            if parts:
                class_counts[parts[0]] += 1
                total_objects += 1
    return class_counts, annotated_images, negative_images, total_objects


def image_size_stats(root: Path, max_images: int = 500):
    sizes = Counter()
    for idx, img_path in enumerate(iter_files(root, IMAGE_EXTS)):
        if idx >= max_images:
            break
        try:
            with Image.open(img_path) as im:
                sizes[f"{im.width}x{im.height}"] += 1
        except Exception:
            continue
    return sizes


def flags(ds):
    text = " ".join(str(v).lower() for v in ds.values())
    return {
        "night": "night" in text or "low-light" in text,
        "rain_water": "rain" in text or "water" in text or "wet" in text,
        "uav": "uav" in text or "aerial" in text,
        "stereo_depth": "stereo" in text or "rgb-d" in text or "disparity" in text or "depth" in text,
        "mask": "mask" in text or "segmentation" in text,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate dataset statistics report.")
    add_common_args(parser)
    parser.add_argument("--config", type=Path, default=project_root() / "configs" / "datasets.yaml")
    parser.add_argument("--converted-root", type=Path, default=project_root() / "converted")
    parser.add_argument("--out", type=Path, default=project_root() / "docs" / "dataset_statistics.md")
    args = parser.parse_args()
    setup_logging(args.verbose)

    lines = ["# Dataset Statistics", "", "Statistics are based on currently available local files. Missing datasets are reported as zero-count placeholders.", ""]
    lines.append("| Dataset | Images | Labels/Ann files | Objects | Potholes | Negative labels | Top image sizes | Night | Rain/Water | UAV | Stereo/Depth | Mask | YOLO detect | YOLO segment |")
    lines.append("|---|---:|---:|---:|---:|---:|---|---|---|---|---|---|---|---|")

    for ds in load_datasets(args.config):
        raw_dir = resolve_path(ds["raw_dir"])
        converted_dir = args.converted_root / ds["name"]
        stats = count_files(raw_dir)
        label_root = converted_dir / "labels" if (converted_dir / "labels").exists() else converted_dir
        cls_counts, ann_imgs, neg_imgs, objects = yolo_label_stats(label_root) if converted_dir.exists() else (Counter(), 0, 0, 0)
        size_counts = image_size_stats(raw_dir)
        top_sizes = ", ".join(f"{k}:{v}" for k, v in size_counts.most_common(3)) or "-"
        f = flags(ds)
        detect_ok = "yes" if converted_dir.exists() and any(iter_files(label_root, {".txt"})) else "no"
        segment_ok = "yes" if f["mask"] else "possible_after_mask_conversion"
        potholes = cls_counts.get("0", 0) if "pothole" in [str(c).lower() for c in ds.get("classes", [])] or "D40" in ds.get("classes", []) else 0
        ann_files = stats["xml"] + stats["json"] + stats["txt"] + stats["mask_like_png"]
        lines.append(f"| {ds['name']} | {stats['images']} | {ann_files} | {objects} | {potholes} | {neg_imgs} | {top_sizes} | {f['night']} | {f['rain_water']} | {f['uav']} | {f['stereo_depth']} | {f['mask']} | {detect_ok} | {segment_ok} |")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
