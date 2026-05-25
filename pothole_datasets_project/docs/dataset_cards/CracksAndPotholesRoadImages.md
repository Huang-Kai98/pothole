# CracksAndPotholesRoadImages
## Source
https://biankatpas.github.io/Cracks-and-Potholes-in-Road-Images-Dataset/

## Download
Status: `manual_download_required`

Command: `manual_download_required`

Expected raw path: `raw/CracksAndPotholesRoadImages`

## Task Type
semantic_segmentation

## Annotation Format
semantic mask

## Classes
road, crack, pothole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Road, crack, and pothole mask classes

## Recommended Usage
Joint drivable-road and pothole segmentation

## Limitations
Manual download and class color-map verification required

## License / Usage Restriction
Check project page terms

## Citation
Cite project page / associated paper

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
