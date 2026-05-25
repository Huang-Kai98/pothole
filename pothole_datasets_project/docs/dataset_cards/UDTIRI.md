# UDTIRI
## Source
jiahangli617/udtiri

## Download
Status: `not_downloaded`

Command: `kaggle datasets download -d jiahangli617/udtiri -p raw/UDTIRI --unzip`

Expected raw path: `raw/UDTIRI`

## Task Type
object_detection; semantic_segmentation; instance_segmentation

## Annotation Format
COCO JSON; masks

## Classes
pothole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
RGB pothole images; suitable for detection and segmentation

## Recommended Usage
Instance/semantic segmentation and VLM benchmarking

## Limitations
Kaggle access and dataset terms required

## License / Usage Restriction
Check Kaggle dataset terms

## Citation
Cite UDTIRI dataset page

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
