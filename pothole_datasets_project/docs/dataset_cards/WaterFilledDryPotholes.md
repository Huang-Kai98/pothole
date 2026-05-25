# WaterFilledDryPotholes
## Source
Mendeley Data DOI: 10.17632/tp95cdvgm8.1

## Download
Status: `manual_download_required`

Command: `manual_download_required`

Expected raw path: `raw/WaterFilledDryPotholes`

## Task Type
object_detection

## Annotation Format
Pascal VOC XML; YOLO TXT

## Classes
pothole

## Scale
Current local scan: total_files: 0, images: 0, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Water-filled and dry potholes

## Recommended Usage
Wet-road and post-rain robustness

## Limitations
Manual download recommended

## License / Usage Restriction
Check Mendeley Data terms

## Citation
Mendeley Data DOI: 10.17632/tp95cdvgm8.1

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
