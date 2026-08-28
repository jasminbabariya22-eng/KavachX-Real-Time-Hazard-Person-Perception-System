# Model Overview & Architecture

## 1. Model Specifications

| Parameter | Specification |
| :--- | :--- |
| **Model Family** | YOLOv8-Style Object Detector |
| **Input Shape** | $[1, 3, 640, 640]$ NCHW |
| **Input DataType** | `uint8` ($[0\dots255]$ RGB) |
| **Quantization Format** | Symmetric INT8 (Qualcomm QNN HTP format) |
| **Target Classes (3)** | `0: fire`, `1: smoke`, `2: person` |
| **Production Artifact** | `models/production/3class_calibrated_final.bin` ($26.8	ext{ MB}$) |
| **SHA256 Checksum** | `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc` |
| **Reference Model** | `models/reference/new_3class_best_FP32_htp_split.onnx` ($103.4	ext{ MB}$) |

---

## 2. Model Split Architecture for Hexagon HTP

To resolve the dynamic DFL slice blocker on Qualcomm Hexagon DSPs, the network graph is partitioned:

```text
[Input: 1x3x640x640 uint8]
             │
             ▼
┌──────────────────────────────────────────────────────────┐
│  Qualcomm Hexagon v68 HTP Context Binary (NPU)           │
│  - CSPDarknet Backbone (Conv, C2f, SPPF)                 │
│  - PANet Neck (Upsample, Concat, C2f)                    │
│  - Multi-Scale Convolutional Detection Heads             │
└────────────────────────────┬─────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [output_0: 1x64x8400 uint8]       [output_1: 1x3x8400 uint8]
   (DFL Box Distributions)           (Class Probabilities)
            │                                 │
            └────────────────┬────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────┐
│  CPU Vectorized Postprocessor (C++ / Python)             │
│  - Softmax & expectation over 16 DFL bins per coordinate │
│  - Grid anchor multiplication & unletterboxing           │
│  - Confidence filtering (conf >= 0.25) & NMS             │
└──────────────────────────────────────────────────────────┘
```
