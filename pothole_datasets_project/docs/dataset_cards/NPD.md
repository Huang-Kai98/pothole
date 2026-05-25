# NPD
## Source
https://github.com/hhaozhang/NPD

## Download
Status: `not_downloaded`

Command: `gdown --id 1F7IBMEwf25ZVgJC2RrqbCbiuZM-wc1f0 -O raw/NPD/npd_archive`

Expected raw path: `raw/NPD`

## Task Type
object_detection

## Annotation Format
Check dataset release

## Classes
pothole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Nighttime and low-light pothole detection

## Recommended Usage
Night/low-light robustness evaluation

## Limitations
Usage restrictions; annotation format should be checked after download

## License / Usage Restriction
Non-commercial research use; check repository

## Citation
Cite NPD GitHub / paper if provided

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
