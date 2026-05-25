# HRP4K
## Source
Zenodo / paper data page

## Download
Status: `manual_download_required`

Command: `manual_download_required`

Expected raw path: `raw/HRP4K`

## Task Type
object_detection

## Annotation Format
YOLO TXT; COCO JSON

## Classes
pothole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
4K high-resolution road images; positive and negative samples; small potholes

## Recommended Usage
Small-object pothole detection and high-resolution robustness evaluation

## Limitations
Automatic stable URL not configured; verify license and citation manually

## License / Usage Restriction
Check source page before use

## Citation
Cite HRP4K paper and dataset page

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
