# HRP4K
## Source
https://doi.org/10.5281/zenodo.17522874

## Download
Status: `not_downloaded`

Command: `python scripts/download_zenodo.py --dataset HRP4K`

Expected raw path: `raw/HRP4K`

## Task Type
object_detection

## Annotation Format
YOLO TXT; COCO JSON

## Classes
pothole

## Scale
Current local scan: total_files: 10092, images: 4086, xml: 0, json: 3, txt: 6003, mask_like_png: 0

## Scene Characteristics
4K high-resolution road images; positive and negative samples; small potholes

## Recommended Usage
Small-object pothole detection and high-resolution robustness evaluation

## Limitations
Large download; verify train/val/test split and annotation folder layout after extraction

## License / Usage Restriction
CC BY 4.0

## Citation
HRP4K, Zenodo DOI: 10.5281/zenodo.17522874; cite the Scientific Data paper

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
