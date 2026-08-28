# KavachX System Architecture

## 1. Executive System Overview
KavachX is an industrial-grade edge perception appliance engineered for continuous, real-time detection of **Fire, Smoke, and Persons**. The system is deployed on the **Qualcomm QCS6490 SoC** (Radxa Dragon Q6490), offloading 100% of deep learning tensor execution to the **Qualcomm Hexagon v68 HTP DSP** via FastRPC.

```mermaid
flowchart TD
    subgraph INGESTION["1. INPUT INGESTION LAYER"]
        CAM_V4L2["Physical USB / CSI Camera\n(/dev/video0)"]
        CAM_RTSP["RTSP Network IP Camera\n(rtsp://...)"]
        CAM_FILE["Synthetic / File Stream\n(test_data/videos/...)"]
    end

    subgraph ADAPTERS["2. CAPTURE ADAPTERS (src/kavachx/capture)"]
        CAM_V4L2 --> V4L2_SRC["V4L2Source"]
        CAM_RTSP --> RTSP_SRC["RTSPSource\n(Auto-Reconnect Loop)"]
        CAM_FILE --> VIDEO_SRC["VideoSource\n(Looping Video Driver)"]
    end

    subgraph PIPELINE["3. PIPELINE & QUEUE (src/kavachx/pipeline)"]
        V4L2_SRC & RTSP_SRC & VIDEO_SRC --> BQ["Bounded Frame Queue\n(maxsize=2, Latest-Frame-Wins Policy)"]
        BQ --> PREPROC["Aspect-Preserving Letterbox\n[1, 3, 640, 640] uint8 NCHW"]
    end

    subgraph IPC_LAYER["4. BINARY IPC TRANSPORT (src/kavachx/ipc)"]
        PREPROC --> IPC_CLI["UNIX Socket Client\n(/tmp/kawach_worker.sock)"]
    end

    subgraph NATIVE_WORKER["5. NATIVE C++ WORKER DAEMON (native/worker)"]
        IPC_CLI --> IPC_SRV["Non-Blocking UNIX Socket Server\n(Framing: Magic 0x4B574158 / 0x5841574B)"]
        IPC_SRV --> QNN_LOADER["QNN HTP Runtime Loader\n(libQnnHtp.so / libQnnSystem.so)"]
        QNN_LOADER --> FASTRPC["Qualcomm FastRPC Bridge\n(/dev/fastrpc-cdsp, GID 993 render)"]
    end

    subgraph HARDWARE_DSP["6. NEURAL HARDWARE ACCELERATOR"]
        FASTRPC --> HTP_DSP["Qualcomm Hexagon v68 HTP DSP\n(INT8 Context Binary: 3class_calibrated_final.bin)\n- CSPDarknet Backbone\n- PANet Feature Neck\n- Multi-Scale Conv Heads\n[100% Neural Execution | 0 CPU Fallback]"]
        HTP_DSP --> TENSOR_OUT["Static Output Tensors:\n- output_0: [1, 64, 8400] uint8 (DFL Bins)\n- output_1: [1, 3, 8400] uint8 (Class Scores)"]
    end

    subgraph POSTPROCESSING["7. CPU POSTPROCESSING & EVENT DISPATCH"]
        TENSOR_OUT --> IPC_SRV
        IPC_SRV --> IPC_CLI
        IPC_CLI --> DFL_DEC["Vectorized DFL Box Decoder (CPU: <1 ms)\ncoord = SUM(i * Softmax(bin_i))\nUnletterbox Coordinates -> Original Resolution"]
        DFL_DEC --> NMS["Non-Maximum Suppression (NMS)\n(IoU Threshold: 0.45, Conf: 0.25)"]
        NMS --> EVENT_MGR["Alert Event Manager\n(3.0s Debounce Cooldown)"]
        EVENT_MGR --> ALERTS["🚨 Fire: CRITICAL HAZARD\n⚠️ Smoke: WARNING HAZARD\n⚠️ Person: WARNING OCCUPANCY"]
    end
```

---

## 2. Structural Layer Responsibilities

| Layer | Implementation Directory | Language / Engine | Primary Responsibility |
| :--- | :--- | :---: | :--- |
| **Ingestion** | `src/kavachx/capture/` | Python / OpenCV | Abstraction of V4L2 device nodes, RTSP RTSP streams, and video files. |
| **Pipeline & Queue** | `src/kavachx/pipeline/` | Python / Threading | Asynchronous capture, queue bounding (`maxsize=2`), and latest-frame drop policy. |
| **Preprocessing** | `src/kavachx/inference/postprocess.py` | Vectorized NumPy | Aspect-ratio letterbox padding to $[1, 3, 640, 640]$ uint8 RGB buffer. |
| **IPC Protocol** | `src/kavachx/ipc/` | Binary C-Types Socket | Framed low-overhead UNIX stream socket communication over `/tmp/kawach_worker.sock`. |
| **Native Daemon** | `native/worker/` | C++11 (GCC 9.4+ ARM64) | QNN context binary loading, FastRPC memory management, and request dispatch. |
| **Hardware DSP** | `models/production/` | Qualcomm Hexagon HTP | $100\%$ neural execution on Hexagon v68 DSP ($\sim 30\text{ ms}$ inference). |
| **Postprocessing** | `src/kavachx/inference/decoder.py` | Vectorized NumPy | DFL expectation math, coordinate unletterboxing, and class filtering. |
| **Event Dispatch** | `src/kavachx/pipeline/events.py` | Python Logic | Debounced event classification and alerting. |
