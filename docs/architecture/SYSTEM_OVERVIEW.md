# System Overview & Architecture

## 1. Purpose & Problem Statement
KavachX is an edge-deployed computer vision system for continuous industrial safety monitoring. It detects **Fire, Smoke, and Persons** entirely on-device without reliance on cloud connectivity.

Deployed on the **Qualcomm QCS6490 SoC** (Radxa Dragon Q6490), the system offloads 100% of deep learning tensor computations to the **Qualcomm Hexagon v68 HTP DSP** via FastRPC (`/dev/fastrpc-cdsp`), achieving zero CPU/GPU neural network fallback while preserving host CPU cores for multi-camera video ingestion and alert dispatching.

---

## 2. High-Level Architecture Flowchart

```mermaid
flowchart TD
    subgraph INGESTION["1. Ingestion Layer (src/kavachx/capture)"]
        CAM_USB["Physical USB / CSI Camera\n(/dev/video0)"]
        CAM_RTSP["RTSP Network IP Camera\n(rtsp://...)"]
        CAM_FILE["Synthetic / File Stream\n(test_data/videos/...)"]
    end

    subgraph PIPELINE["2. Pipeline & Queue (src/kavachx/pipeline)"]
        CAM_USB & CAM_RTSP & CAM_FILE --> BQ["Bounded Frame Queue\n(maxsize=2, Drop-Stale Policy)"]
        BQ --> PREPROC["Aspect-Preserving Letterbox\n[1, 3, 640, 640] uint8 NCHW"]
    end

    subgraph IPC_LAYER["3. Binary IPC Transport (src/kavachx/ipc)"]
        PREPROC --> IPC_CLI["UNIX Socket Client\n(/tmp/kawach_worker.sock)"]
    end

    subgraph NATIVE_DAEMON["4. Native C++ Worker (native/worker)"]
        IPC_CLI --> IPC_SRV["Non-Blocking Socket Server\n(Framing: 0x4B574158 / 0x5841574B)"]
        IPC_SRV --> QNN_LOADER["QNN HTP Runtime Loader\n(libQnnHtp.so / libQnnSystem.so)"]
        QNN_LOADER --> FASTRPC["FastRPC Kernel Transport\n(/dev/fastrpc-cdsp, GID 993 render)"]
    end

    subgraph DSP_ENGINE["5. Neural Hardware Acceleration"]
        FASTRPC --> HTP_DSP["Qualcomm Hexagon v68 HTP DSP\n(INT8 Context: 3class_calibrated_final.bin)\n- CSPDarknet Backbone\n- PANet Neck\n- Multi-Scale Conv Heads\n[100% DSP Execution | 0 CPU Fallback]"]
        HTP_DSP --> TENSORS["Output Tensors:\n- output_0: [1, 64, 8400] uint8 (DFL Bins)\n- output_1: [1, 3, 8400] uint8 (Class Scores)"]
    end

    subgraph CPU_POSTPROC["6. CPU Postprocessing & Event Dispatch"]
        TENSORS --> IPC_SRV
        IPC_SRV --> IPC_CLI
        IPC_CLI --> DFL_DEC["Vectorized DFL Box Decoder (CPU: <1 ms)\ncoord = SUM(i * Softmax(bin_i))\nUnletterbox Coordinates -> Original Resolution"]
        DFL_DEC --> NMS["Non-Maximum Suppression (NMS)\n(IoU Threshold: 0.45, Conf: 0.25)"]
        NMS --> EVENT_MGR["Alert Event Manager\n(3.0s Debounce Cooldown)"]
        EVENT_MGR --> ALERTS["🚨 Fire: CRITICAL HAZARD\n⚠️ Smoke: WARNING HAZARD\n⚠️ Person: WARNING OCCUPANCY"]
    end
```
