# RoboflowKagglePothole
## Source
andrewmvd/pothole-detection

## Download
Status: `not_downloaded`

Command: `kaggle datasets download -d andrewmvd/pothole-detection -p raw/RoboflowKagglePothole --unzip`

Expected raw path: `raw/RoboflowKagglePothole`

## Task Type
object_detection

## Annotation Format
Check dataset release; often YOLO/COCO variants

## Classes
pothole

## Scale
Current local scan: total_files: 1330, images: 665, xml: 665, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Small pothole detection dataset

## Recommended Usage
Quick demos and smoke tests, not main benchmark

## Limitations
Small scale and possible redistribution constraints

## License / Usage Restriction
Check Kaggle dataset terms

## Citation
Cite Kaggle dataset page

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
