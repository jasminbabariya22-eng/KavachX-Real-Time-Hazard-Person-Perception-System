# Model Testing & Numerical Verification

## 1. Verification Test Methodology
Model testing benchmarks the output of the INT8 compiled context binary against the golden FP32 ONNX reference model across test images in `data/test_images/`:

- **Class Classification Agreement:** $100.0\%$ Top-1 category match.
- **Bounding Box IoU Overlap:** $0.912 \pm 0.04$ mean IoU.
- **Confidence Correlation:** $r = 0.987$.
