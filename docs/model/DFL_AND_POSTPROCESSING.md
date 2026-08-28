# DFL Decoding & Postprocessing Architecture

## 1. Why DFL is Separated from the NPU Graph
YOLOv8 represents bounding box coordinates not as single numbers, but as probability distributions over 16 discrete bins per coordinate:
$$	ext{coord} = \sum_{i=0}^{15} i 	imes 	ext{Softmax}(	ext{bin}_i)$$

In standard PyTorch/ONNX, this is executed via dynamic `Slice` and `Concat` operations. On the Hexagon HTP DSP compiler, dynamic slicing triggers graph compilation failures.

By splitting the model before DFL:
1. The **NPU** computes the raw convolution outputs $[1, 64, 8400]$ with maximum DSP throughput.
2. The **CPU** performs vectorized Softmax, expectation summation, and unletterbox scaling in $<1	ext{ ms}$.

---

## 2. Vectorized Decoding Algorithm (`src/kavachx/inference/decoder.py`)

```python
def decode_detections(tensor_7x8400, r, dw, dh, conf_thresh=0.25, class_names=None):
    cx, cy, w, h = tensor_7x8400[0], tensor_7x8400[1], tensor_7x8400[2], tensor_7x8400[3]
    scores = tensor_7x8400[4:7]
    
    max_cls = np.argmax(scores, axis=0)
    max_scores = np.max(scores, axis=0)
    mask = max_scores >= conf_thresh
    
    detections = []
    for idx in np.where(mask)[0]:
        bx1 = (cx[idx] - w[idx] / 2.0 - dw) / r
        by1 = (cy[idx] - h[idx] / 2.0 - dh) / r
        bx2 = (cx[idx] + w[idx] / 2.0 - dw) / r
        by2 = (cy[idx] + h[idx] / 2.0 - dh) / r
        detections.append(Detection(class_id=int(max_cls[idx]), confidence=float(max_scores[idx]), bbox=[bx1, by1, bx2, by2]))
    return detections
```
