# RuiFanStereoPothole
## Source
https://github.com/ruirangerfan/stereo_pothole_datasets

## Download
Status: `not_downloaded`

Command: `git clone https://github.com/ruirangerfan/stereo_pothole_datasets raw/RuiFanStereoPothole`

Expected raw path: `raw/RuiFanStereoPothole`

## Task Type
stereo_detection; segmentation; 3D

## Annotation Format
rgb; disparity; transformed disparity; pixel-level labels; point cloud

## Classes
pothole

## Scale
Current local scan: total_files: 405, images: 268, xml: 0, json: 0, txt: 0, mask_like_png: 0

## Scene Characteristics
Stereo data with labels and point clouds

## Recommended Usage
3D pothole perception and depth-assisted avoidance

## Limitations
Large files may require Git LFS or manual links

## License / Usage Restriction
Check GitHub repository license

## Citation
Cite repository and associated papers

## Conversion Notes
Use the matching converter based on `annotation_format`. For RDD-family datasets, use `scripts/convert_rdd_d40_to_yolo.py` to map `D40` to `pothole`. For segmentation masks, inspect pixel values before running `scripts/convert_masks_to_yolo_seg.py`.
