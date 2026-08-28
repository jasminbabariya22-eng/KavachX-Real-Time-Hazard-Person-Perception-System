# Model Architecture Visual Summary

## 1. Quick Reference Properties

| Parameter | Authoritative Value | Verification Reference |
| :--- | :--- | :--- |
| **Model Family** | YOLOv8 Split-Head Detector | `models/production/3class_calibrated_final.bin` |
| **Input Shape** | $[1, 3, 640, 640]$ uint8 NCHW | Verified via QNN C API tensor descriptor |
| **Target Classes** | `0: fire`, `1: smoke`, `2: person` | `config/production.json` |
| **Quantization Format** | Symmetric INT8 (Per-Channel Weights) | Compiled with QAIRT 2.47 |
| **Context Binary Size** | $26,800,128\text{ bytes}$ ($26.8\text{ MB}$) | File inspection |
| **Context SHA256** | `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc` | Checksum verification |
| **DSP Execution** | $100\%$ on Qualcomm Hexagon v68 HTP | `tests/hardware/test_htp_inference.py` |
| **Host CPU Postprocessing**| Vectorized DFL expectation & NMS | `src/kavachx/inference/decoder.py` |
