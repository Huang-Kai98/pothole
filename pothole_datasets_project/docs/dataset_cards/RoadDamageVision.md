# RoadDamageVision
## Source
Mendeley Data DOI: 10.17632/ypm4h4z25c.3

## Download
Status: `manual_download_required`

Command: `manual_download_required`

Expected raw path: `raw/RoadDamageVision`

## Task Type
object_detection

## Annotation Format
Check dataset release

## Classes
D00, D10, D20, D40

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Road damage detection with D40 potholes

## Recommended Usage
Domain adaptation and class imbalance experiments

## Limitations
Manual download and label schema verification required

## License / Usage Restriction
Check Mendeley Data terms

## Citation
Mendeley Data DOI: 10.17632/ypm4h4z25c.3

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
