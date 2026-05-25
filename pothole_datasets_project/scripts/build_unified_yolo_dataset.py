#!/usr/bin/env python3
import argparse
import logging
import random
import shutil
from collections import defaultdict
from pathlib import Path

from common import IMAGE_EXTS, add_common_args, iter_files, project_root, save_yaml, setup_logging, write_json


def collect_pairs(converted_root: Path):
    pairs = []
    for ds_dir in sorted(p for p in converted_root.iterdir() if p.is_dir()) if converted_root.exists() else []:
        image_dirs = [p for p in [ds_dir / "images", ds_dir] if p.exists()]
        label_dirs = [p for p in [ds_dir / "labels", ds_dir] if p.exists()]
        labels = {}
        for label_dir in label_dirs:
            for label in iter_files(label_dir, {".txt"}):
                labels.setdefault(label.stem, label)
        for image_dir in image_dirs:
            for image in iter_files(image_dir, IMAGE_EXTS):
                label = labels.get(image.stem)
                pairs.append({"dataset": ds_dir.name, "image": image, "label": label})
    return pairs


def split_dataset_names(dataset_names, train, val, seed):
    names = sorted(set(dataset_names))
    random.Random(seed).shuffle(names)
    n = len(names)
    n_train = max(1, int(n * train)) if n else 0
    n_val = max(0, int(n * val))
    train_names = set(names[:n_train])
    val_names = set(names[n_train:n_train + n_val])
    test_names = set(names[n_train + n_val:])
    if not test_names and val_names:
        test_names.add(val_names.pop())
    return train_names, val_names, test_names


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a unified YOLO dataset from converted per-dataset folders.")
    add_common_args(parser)
    parser.add_argument("--converted-root", type=Path, default=project_root() / "converted")
    parser.add_argument("--out-root", type=Path, default=project_root() / "unified_yolo")
    parser.add_argument("--train", type=float, default=0.8)
    parser.add_argument("--val", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--copy", action="store_true", help="Copy files instead of symlinking.")
    parser.add_argument("--classes", nargs="+", default=["pothole"])
    args = parser.parse_args()
    setup_logging(args.verbose)

    pairs = collect_pairs(args.converted_root)
    if not pairs:
        logging.warning("No converted image/label pairs found under %s.", args.converted_root)
    train_names, val_names, test_names = split_dataset_names([p["dataset"] for p in pairs], args.train, args.val, args.seed)
    split_for_ds = {name: "train" for name in train_names} | {name: "val" for name in val_names} | {name: "test" for name in test_names}

    manifest = []
    for split in ["train", "val", "test"]:
        (args.out_root / "images" / split).mkdir(parents=True, exist_ok=True)
        (args.out_root / "labels" / split).mkdir(parents=True, exist_ok=True)

    counts = defaultdict(int)
    for item in pairs:
        split = split_for_ds.get(item["dataset"], "train")
        prefix = item["dataset"]
        out_img = args.out_root / "images" / split / f"{prefix}__{item['image'].name}"
        out_lbl = args.out_root / "labels" / split / f"{prefix}__{item['image'].stem}.txt"
        if out_img.exists():
            out_img.unlink()
        if args.copy:
            shutil.copy2(item["image"], out_img)
        else:
            out_img.symlink_to(item["image"].resolve())
        if item["label"] and item["label"].exists():
            if out_lbl.exists():
                out_lbl.unlink()
            if args.copy:
                shutil.copy2(item["label"], out_lbl)
            else:
                out_lbl.symlink_to(item["label"].resolve())
        else:
            out_lbl.write_text("", encoding="utf-8")
        counts[split] += 1
        manifest.append({"dataset": item["dataset"], "split": split, "image": str(out_img), "label": str(out_lbl)})

    save_yaml({"path": str(args.out_root.resolve()), "train": "images/train", "val": "images/val", "test": "images/test", "names": {i: c for i, c in enumerate(args.classes)}}, args.out_root / "data.yaml")
    write_json(manifest, args.out_root / "manifest.json")
    logging.info("Unified dataset counts: %s", dict(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
