# Model Architecture & Specifications

## 1. Specification Baseline

| Parameter | Specification | Verification Source |
| :--- | :--- | :--- |
| **Model Family** | YOLOv8-Style Split-Head Detector | `models/production/3class_calibrated_final.bin` |
| **Input Shape** | $[1, 3, 640, 640]$ NCHW | Verified via QNN C API tensor descriptor |
| **Input DataType** | `uint8` ($[0\dots255]$ RGB) | Preprocessor contract |
| **Target Classes (3)** | `0: fire`, `1: smoke`, `2: person` | `config/production.json` |
| **Production Artifact** | `models/production/3class_calibrated_final.bin` ($26.8\text{ MB}$) | File inspection |
| **SHA256 Checksum** | `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc` | Checksum verification |
| **Reference Model** | `models/reference/new_3class_best_FP32_htp_split.onnx` ($103.4\text{ MB}$) | Baseline model |
