# Model Architecture & Tensor Contract

## 1. Visual Model Flow & Tensor Dimensions

```mermaid
flowchart TD
    INPUT["Input RGB Image\n(1920x1080 Camera Stream)"] --> PREPROC["Aspect-Preserving Letterbox\nTransposed to NCHW"]
    
    subgraph TENSOR_INPUT["Model Input Tensor"]
        IN_TENSOR["images: [1, 3, 640, 640] uint8\nScale: 1.0, Offset: 0"]
    end
    PREPROC --> IN_TENSOR

    subgraph HTP_GRAPH["Qualcomm Hexagon HTP Quantized Model (INT8)"]
        BACKBONE["CSPDarknet Backbone\n(Conv, C2f, SPPF)"]
        NECK["PANet Multi-Scale Feature Neck\n(Upsample, Concat, C2f)"]
        HEADS["Multi-Scale Convolutional Heads\n(P3/8, P4/16, P5/32 Scales)"]
        
        IN_TENSOR --> BACKBONE
        BACKBONE --> NECK
        NECK --> HEADS
    end

    subgraph TENSOR_OUTPUTS["Static Output Tensors"]
        HEADS --> OUT_0["output_0: [1, 64, 8400] uint8\n(4 coords * 16 DFL Distribution Bins)"]
        HEADS --> OUT_1["output_1: [1, 3, 8400] uint8\n(Class Sigmoid Scores: fire, smoke, person)"]
    end

    subgraph CPU_DECODER["Vectorized CPU Postprocessor (src/kavachx/inference/decoder.py)"]
        OUT_0 & OUT_1 --> SOFTMAX["Vectorized DFL Softmax & Expectation\ncoord = SUM(i * Softmax(bin_i))"]
        SOFTMAX --> UNLETTERBOX["Coordinate Scaling & Unletterbox\nx = (x_lb - dw) / r,  y = (y_lb - dh) / r"]
        UNLETTERBOX --> NMS_FILTER["Confidence Filtering (>= 0.25) & NMS (IoU >= 0.45)"]
    end

    subgraph DETECTIONS["Final Detections"]
        NMS_FILTER --> DET_OBJ["Detection(class_id, confidence, bbox=[x1, y1, x2, y2])\n- FIRE (Class 0)\n- SMOKE (Class 1)\n- PERSON (Class 2)"]
    end
```

---

## 2. Static Tensor Specifications

| Tensor Name | Direction | Tensor Shape | Data Type | Encoding Details | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `images` | Input | $[1, 3, 640, 640]$ | `uint8` | Scale: $1.0$, Offset: $0$ | Raw RGB letterboxed image buffer. |
| `output_0` | Output | $[1, 64, 8400]$ | `uint8` | Quantized DFL distributions | 4 coordinates $\times$ 16 distribution bins across 8400 anchors. |
| `output_1` | Output | $[1, 3, 8400]$ | `uint8` | Quantized sigmoid probabilities | Class scores for `fire`, `smoke`, and `person`. |
