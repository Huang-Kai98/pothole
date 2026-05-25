# RoadDamagePotholesCracksManholes
## Source
lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes

## Download
Status: `not_downloaded`

Command: `kaggle datasets download -d lorenzoarcioni/road-damage-dataset-potholes-cracks-and-manholes -p raw/RoadDamagePotholesCracksManholes --unzip`

Expected raw path: `raw/RoadDamagePotholesCracksManholes`

## Task Type
object_detection

## Annotation Format
YOLO TXT

## Classes
pothole, crack, manhole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Road damage with potholes, cracks, and manholes

## Recommended Usage
Hard-negative training to reduce manhole/pothole confusion

## Limitations
Verify class order before conversion or unification

## License / Usage Restriction
Check Kaggle dataset terms

## Citation
Cite Kaggle dataset page

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
