# KavachX Technology Stack

This document specifies the complete, verified technology stack utilized across all subsystems of KavachX.

---

## 1. Subsystem Technology Matrix

| Subsystem | Technology | Purpose | Location in Repository |
| :--- | :--- | :--- | :--- |
| **Target Hardware** | Qualcomm QCS6490 SoC | 8-core Kryo 670 CPU (2.7 GHz) + Adreno 643 GPU + Hexagon v68 HTP DSP. | Physical Appliance Board |
| **Neural Accelerator** | Qualcomm Hexagon v68 HTP DSP | High-efficiency INT8 vector & tensor acceleration. | Hardware Processor |
| **Hardware Transport** | Qualcomm FastRPC (`/dev/fastrpc-cdsp`) | Zero-copy shared-memory kernel transport to cDSP. | `/dev/fastrpc-cdsp` (GID `993`) |
| **NPU SDK Runtime** | Qualcomm QAIRT / QNN SDK 2.47.0.260601 | HTP runtime backend (`libQnnHtp.so`, `libQnnSystem.so`). | Target System Path |
| **Machine Learning Base**| YOLOv8-Style Object Detector | Split-head 3-class detection (`fire`, `smoke`, `person`). | `models/` |
| **Reference Format** | ONNX (FP32) | Golden baseline model for numerical parity validation. | `models/reference/` |
| **Production Format** | Serialized QNN Context Binary (`.bin`) | Calibrated INT8 context binary ($26.8\text{ MB}$). | `models/production/` |
| **Native Runtime** | C++11 (`g++` ARM64) | FastRPC worker daemon serving UNIX socket requests. | `native/worker/` |
| **Inter-Process Comm** | UNIX Domain Stream Socket | Low-latency binary framed IPC (`/tmp/kawach_worker.sock`). | `src/kavachx/ipc/`, `native/worker/` |
| **Python Runtime** | Python 3.10 / 3.12 (`aarch64` / `x86_64`) | Ingestion pipeline, DFL decoding, and event dispatch. | `src/kavachx/` |
| **Image Processing** | OpenCV Headless (`opencv-python-headless`) | Video capture, frame decoding, and color conversion. | `src/kavachx/capture/` |
| **Math & Tensors** | NumPy (`numpy>=1.20.0`) | Vectorized letterboxing, DFL Softmax, and NMS. | `src/kavachx/inference/` |
| **Supervisor Service** | Python Supervisor Daemon | Process monitoring, pre-flight checks, auto-restart. | `tools/service_manager.py` |
| **Deployment Engine** | Systemd & Shell Scripts | Service lifecycle and turnkey installation. | `config/`, `deployment/` |
| **Testing Engine** | Python PyTest & Custom Suites | Multi-tier hardware, streaming, and integration tests. | `tests/` |
