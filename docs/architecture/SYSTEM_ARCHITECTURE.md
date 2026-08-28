# KavachX System Architecture

## 1. Purpose & Problem Statement
KavachX is an enterprise edge computer vision appliance designed for continuous industrial safety monitoring. It detects **Fire, Smoke, and Persons** entirely on-device without cloud dependency.

The system is deployed on the **Qualcomm QCS6490 SoC** (Radxa Dragon Q6490 / Kavach-EdgeBox). To operate 24/7 within strict thermal envelopes while leaving CPU headroom for multi-camera video decoding and alert dispatching, all deep learning inference is offloaded to the **Qualcomm Hexagon v68 HTP DSP**.

---

## 2. High-Level System Architecture

```mermaid
flowchart TD
    subgraph INGESTION["1. Ingestion Layer (src/kavachx/capture)"]
        CAM_USB["Physical USB / CSI Camera
(/dev/video0)"] --> ADAPT["Camera Adapter"]
        CAM_RTSP["RTSP Network IP Camera
(rtsp://...)"] --> ADAPT
        CAM_FILE["Video File Stream
(test_data/videos/...)"] --> ADAPT
    end

    subgraph PIPELINE["2. Live Processing Pipeline (src/kavachx/pipeline)"]
        ADAPT --> BQ["Bounded Frame Queue
(maxsize=2, Drop-Stale Policy)"]
        BQ --> PREPROC["Aspect-Ratio Letterboxing
[1, 3, 640, 640] uint8"]
    end

    subgraph IPC_LAYER["3. IPC Transport (src/kavachx/ipc)"]
        PREPROC --> SOCK_CLI["UNIX Domain Socket Client
(/tmp/kawach_worker.sock)"]
    end

    subgraph NATIVE_WORKER["4. Native C++ Daemon (native/worker)"]
        SOCK_CLI --> SOCK_SRV["Non-Blocking Socket Server
(Framing: 0x4B574158 / 0x5841574B)"]
        SOCK_SRV --> QNN_LOADER["QNN HTP Runtime Loader
(libQnnHtp.so)"]
        QNN_LOADER --> FASTRPC["FastRPC Transport
(/dev/fastrpc-cdsp)"]
        FASTRPC --> DSP["Qualcomm Hexagon v68 HTP DSP
(100% Neural Network Execution)"]
        DSP --> TENSORS["Output Tensors:
output_0: [1, 64, 8400] uint8
output_1: [1, 3, 8400] uint8"]
        TENSORS --> SOCK_SRV
    end

    subgraph DECODING["5. Postprocessing & Alerts (src/kavachx/inference & pipeline)"]
        SOCK_SRV --> DFL["Vectorized DFL Box & Class Decoder (CPU)"]
        DFL --> NMS["Coordinate Unletterbox & NMS"]
        NMS --> EVENTS["Alert Event Manager
(Debounced Dispatches)"]
        EVENTS --> ALERTS["🚨 Fire: CRITICAL
⚠️ Smoke: WARNING
⚠️ Person: WARNING"]
    end
```

---

## 3. Boundary Definitions

### 3.1 Hardware vs. Software Boundary
- **Hexagon v68 HTP DSP:** Executes all convolutional layers, C2f feature extraction blocks, SPPF pooling, and detection head convolution layers ($99.7\%$ of total model FLOPs).
- **Kryo 670 CPU:** Handles video decompression (OpenCV/V4L2), aspect-ratio letterbox padding, DFL coordinate math, and NMS box filtering ($<1	ext{ ms}$).

### 3.2 Python vs. C++ Process Boundary
- **C++ Native Daemon (`native/worker`):** Long-running background daemon holding an open FastRPC session (`/dev/fastrpc-cdsp`). Survives Python client restarts.
- **Python Application (`src/kavachx`):** Stateless client communicating with the daemon over a framed UNIX stream socket (`/tmp/kawach_worker.sock`).
