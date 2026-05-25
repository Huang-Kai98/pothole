# PotholeMix
## Source
Mendeley Data DOI: 10.17632/kfth5g2xk3.2

## Download
Status: `manual_download_required`

Command: `manual_download_required`

Expected raw path: `raw/PotholeMix`

## Task Type
semantic_segmentation

## Annotation Format
image-mask pairs; RGB-D video

## Classes
pothole, crack

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Pothole and crack segmentation; RGB-D video

## Recommended Usage
Segmentation and depth-aware obstacle studies

## Limitations
Manual download and mask convention inspection required

## License / Usage Restriction
Check Mendeley Data terms

## Citation
Mendeley Data DOI: 10.17632/kfth5g2xk3.2

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
