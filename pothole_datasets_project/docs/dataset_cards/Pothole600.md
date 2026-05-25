# Pothole600
## Source
https://sites.google.com/view/pothole-600/dataset

## Download
Status: `manual_download_required`

Command: `manual_download_required`

Expected raw path: `raw/Pothole600`

## Task Type
RGB-D/stereo semantic_segmentation

## Annotation Format
RGB; disparity; segmentation labels

## Classes
pothole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
ZED stereo RGB-D pothole segmentation

## Recommended Usage
Depth-aware obstacle avoidance

## Limitations
Manual download required; stereo calibration assumptions should be checked

## License / Usage Restriction
Check dataset site terms

## Citation
Cite Pothole-600 dataset / paper

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
