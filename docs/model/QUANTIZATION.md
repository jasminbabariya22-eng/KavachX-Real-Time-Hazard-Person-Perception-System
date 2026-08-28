# Model Quantization & Compilation

## 1. Quantization Methodology
Qualcomm Hexagon v68 HTP DSPs operate on fixed-point INT8 arithmetic. The model was converted and compiled using Qualcomm QAIRT / QNN SDK (version `2.47.0.260601`):

1. **Graph Sanitization & Splitting:**
   The dynamic DFL slice tail was removed from the ONNX graph, leaving fixed-size multi-scale head outputs.
2. **Calibration Dataset Generation:**
   A representative dataset of 100 industrial safety images containing fire, smoke, and persons was preprocessed to $[1, 3, 640, 640]$ RGB uint8 format.
3. **QNN Model Conversion (`qnn-onnx-converter`):**
   Converted the split ONNX model into QNN C++ model definitions with quantization encodings.
4. **HTP Context Binary Compilation (`qnn-context-binary-generator`):**
   Compiled the quantized model into the serialized HTP context binary:
   `models/production/3class_calibrated_final.bin` ($26,800,128	ext{ bytes}$).

---

## 2. Quantization Encoding Scheme
- **Input Tensor (`images`):** $[1, 3, 640, 640]$ `uint8`, scale: $1.0$, offset: $0$.
- **Output Tensor 0 (`output_0`):** $[1, 64, 8400]$ `uint8`, representing 4 coordinates $	imes$ 16 DFL distribution bins across 8400 anchor points.
- **Output Tensor 1 (`output_1`):** $[1, 3, 8400]$ `uint8`, representing sigmoid class probabilities for `fire`, `smoke`, and `person`.
