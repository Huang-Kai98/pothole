# Pothole Datasets Project

This project builds a reproducible download, archive, conversion, and reporting workflow for road pothole detection and vision-model-assisted obstacle avoidance datasets.

It intentionally does not train a model and does not blindly mix all sources. Each dataset is kept under `raw/`, converted into a per-dataset folder under `converted/`, and only then linked or copied into `unified_yolo/` with a manifest.

## Setup

```bash
cd pothole_datasets_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Kaggle API

Create a Kaggle API token from your Kaggle account settings and place it at:

```bash
mkdir -p ~/.kaggle
cp /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

Then download configured Kaggle datasets:

```bash
python scripts/download_kaggle.py
```

Configured Kaggle sources:

- `jiahangli617/udtiri`
- `aliabdelmenam/rdd-2022`
- `andrewmvd/pothole-detection`
- `lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes`

## Google Drive And GitHub Downloads

```bash
python scripts/download_gdrive.py --dataset NPD
python scripts/download_github.py --dataset RuiFanStereoPothole
```

`NPD` uses Google Drive file id `1F7IBMEwf25ZVgJC2RrqbCbiuZM-wc1f0`.

## Manual Downloads

Some datasets are marked `manual_download_required` because stable direct links are not guaranteed or licensing requires a human review. Download them from their source page and place the extracted files in the configured path:

- HRP4K: `raw/HRP4K`
- RDD2020, DOI `10.17632/5ty2wb6gvg.1`: `raw/RDD2020`
- Annotated Water-Filled and Dry Potholes, DOI `10.17632/tp95cdvgm8.1`: `raw/WaterFilledDryPotholes`
- Pothole Mix, DOI `10.17632/kfth5g2xk3.2`: `raw/PotholeMix`
- Pothole-600: `raw/Pothole600`
- Cracks and Potholes in Road Images Dataset: `raw/CracksAndPotholesRoadImages`
- MWPD, DOI `10.17632/s5hx9n2jc3.2`: `raw/MWPD`
- UAV RoadAnomaly-YOLO, DOI `10.17632/c6f2b7mx9t.1`: `raw/UAVRoadAnomalyYOLO`
- RoadDamageVision, DOI `10.17632/ypm4h4z25c.3`: `raw/RoadDamageVision`

After downloading or placing data:

```bash
python scripts/check_raw_datasets.py
python scripts/make_dataset_cards.py
python scripts/dataset_statistics.py
```

## Conversion Examples

Pascal VOC XML to YOLO bbox:

```bash
python scripts/convert_voc_to_yolo.py \
  --xml-dir raw/WaterFilledDryPotholes/annotations \
  --image-dir raw/WaterFilledDryPotholes/images \
  --out-label-dir converted/WaterFilledDryPotholes/labels \
  --classes pothole \
  --skip-unknown
```

COCO bbox to YOLO bbox:

```bash
python scripts/convert_coco_to_yolo.py \
  --json raw/UDTIRI/annotations.json \
  --out-label-dir converted/UDTIRI/labels \
  --classes pothole \
  --keep-empty
```

RDD XML with `D40` mapped to `pothole`:

```bash
python scripts/convert_rdd_d40_to_yolo.py \
  --xml-dir raw/RDD2022 \
  --image-dir raw/RDD2022 \
  --out-label-dir converted/RDD2022/labels \
  --mode pothole_only
```

RDD multiclass mode:

```bash
python scripts/convert_rdd_d40_to_yolo.py \
  --xml-dir raw/RDD2022 \
  --image-dir raw/RDD2022 \
  --out-label-dir converted/RDD2022_multiclass/labels \
  --mode multiclass
```

Binary mask to YOLO segmentation polygon:

```bash
python scripts/convert_masks_to_yolo_seg.py \
  --mask-dir raw/PotholeMix/masks \
  --out-label-dir converted/PotholeMix/labels \
  --class-id 0 \
  --min-area 50
```

Place or link the corresponding images under each converted dataset folder, for example:

```text
converted/RDD2022/
  images/
  labels/
```

## Unified YOLO Dataset

Build a manifest-based unified dataset after per-dataset conversion:

```bash
python scripts/build_unified_yolo_dataset.py --classes pothole
```

The script creates:

- `unified_yolo/images/{train,val,test}`
- `unified_yolo/labels/{train,val,test}`
- `unified_yolo/manifest.json`
- `unified_yolo/data.yaml`

Splits are assigned at dataset level to avoid leaking a source dataset across train/val/test. Use this as a controlled baseline; do not assume it is the best experimental split.

## YOLO Training Command

Training is intentionally not started by this project. Once data is reviewed:

```bash
yolo detect train data=unified_yolo/data.yaml model=yolov8n.pt imgsz=640 epochs=100
```

For segmentation data:

```bash
yolo segment train data=unified_yolo/data.yaml model=yolov8n-seg.pt imgsz=640 epochs=100
```

## Reports

- `docs/download_status.md`: downloaded / manual required / missing status.
- `docs/dataset_statistics.md`: image counts, annotation counts, pothole counts, negative labels, dimensions, and scenario flags.
- `docs/dataset_cards/*.md`: source, format, usage, restrictions, citation, and conversion notes per dataset.
- `docs/known_issues.md`: current caveats and verification requirements.

## Class Mapping

Canonical mappings live in `configs/class_mapping.yaml`.

Important mapping:

- `D40` -> `pothole`
- `D00`, `D10`, `D20` -> `crack`
- `manhole` is kept as a hard-negative or multiclass category when supported.
