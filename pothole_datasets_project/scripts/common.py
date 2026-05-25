import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import yaml


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
LABEL_EXTS = {".txt", ".xml", ".json", ".png"}


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_yaml(data: Dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def load_datasets(config_path: Optional[Path] = None) -> List[Dict]:
    cfg = load_yaml(config_path or project_root() / "configs" / "datasets.yaml")
    return cfg.get("datasets", [])


def resolve_path(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else project_root() / p


def iter_files(root: Path, exts: Optional[Iterable[str]] = None) -> Iterable[Path]:
    if not root.exists():
        return
    lower_exts = {e.lower() for e in exts} if exts else None
    for p in root.rglob("*"):
        if ".git" in p.parts or p.name in {".gitkeep", "download_manifest.json"}:
            continue
        if p.is_file() and (lower_exts is None or p.suffix.lower() in lower_exts):
            yield p


def count_files(root: Path) -> Dict[str, int]:
    images = sum(1 for _ in iter_files(root, IMAGE_EXTS)) if root.exists() else 0
    xml = sum(1 for _ in iter_files(root, {".xml"})) if root.exists() else 0
    json_count = sum(1 for _ in iter_files(root, {".json"})) if root.exists() else 0
    txt = sum(1 for _ in iter_files(root, {".txt"})) if root.exists() else 0
    png_masks = sum(1 for p in iter_files(root, {".png"}) if "mask" in p.name.lower() or "label" in p.name.lower()) if root.exists() else 0
    total = sum(1 for _ in iter_files(root)) if root.exists() else 0
    return {"total_files": total, "images": images, "xml": xml, "json": json_count, "txt": txt, "mask_like_png": png_masks}


def file_checksum(path: Path, block_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def write_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_matching_image(stem: str, image_dirs: List[Path]) -> Optional[Path]:
    for d in image_dirs:
        if not d.exists():
            continue
        for ext in IMAGE_EXTS:
            p = d / f"{stem}{ext}"
            if p.exists():
                return p
            p = d / f"{stem}{ext.upper()}"
            if p.exists():
                return p
    return None


def add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser


def yolo_bbox_from_xyxy(xmin: float, ymin: float, xmax: float, ymax: float, width: float, height: float) -> Tuple[float, float, float, float]:
    xmin = max(0.0, min(float(xmin), width))
    xmax = max(0.0, min(float(xmax), width))
    ymin = max(0.0, min(float(ymin), height))
    ymax = max(0.0, min(float(ymax), height))
    bw = max(0.0, xmax - xmin)
    bh = max(0.0, ymax - ymin)
    cx = xmin + bw / 2.0
    cy = ymin + bh / 2.0
    return cx / width, cy / height, bw / width, bh / height


def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def build_alias_map(class_mapping_path: Optional[Path] = None) -> Dict[str, str]:
    mapping = load_yaml(class_mapping_path or project_root() / "configs" / "class_mapping.yaml")
    out = {}
    for canonical, spec in mapping.items():
        out[normalize_name(canonical)] = canonical
        for alias in spec.get("aliases", []):
            out[normalize_name(str(alias))] = canonical
    return out
