# Model Quantization & Compilation Methodology

## 1. Quantization Pipeline

```mermaid
flowchart TD
    FP32_ONNX["FP32 Split ONNX Model\n(new_3class_best_FP32_htp_split.onnx)"] --> CALIB_DATA["Calibration Dataset\n(100 Industrial Fire/Smoke/Person Images)"]
    
    CALIB_DATA --> QNN_CONVERT["qnn-onnx-converter\n- Generate Quantization Encodings\n- Symmetric INT8 per-channel weights"]
    
    QNN_CONVERT --> QNN_GEN["qnn-context-binary-generator\n- Target Backend: libQnnHtp.so (Hexagon v68)\n- Optimize Graph Allocations"]
    
    QNN_GEN --> HTP_BIN["Compiled HTP Context Binary\n(models/production/3class_calibrated_final.bin)\nSize: 26.8 MB | SHA256: b7868a8c43..."]
```

---

## 2. Quantization Encodings
- **Input Tensor (`images`):** $[1, 3, 640, 640]$ `uint8`, scale: $1.0$, offset: $0$.
- **Output Tensor 0 (`output_0`):** $[1, 64, 8400]$ `uint8`, scale & offset mapped to 16 DFL distribution bins.
- **Output Tensor 1 (`output_1`):** $[1, 3, 8400]$ `uint8`, scale & offset mapped to sigmoid class probabilities.
