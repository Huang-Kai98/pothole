# Known Issues

- Mendeley Data pages are kept as manual downloads to avoid hard-coding unstable or license-sensitive direct links.
- Dataset class orders must be verified before merging third-party YOLO labels.
- Mask datasets may use different color maps or instance encodings; inspect pixel values before conversion.
- `build_unified_yolo_dataset.py` creates dataset-level splits to prevent train/val/test leakage across a source dataset, but near-duplicate images inside one source still require dataset-specific deduplication.
