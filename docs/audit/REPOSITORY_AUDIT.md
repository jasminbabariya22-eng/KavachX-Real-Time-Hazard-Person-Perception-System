# KavachX Repository Audit

## 1. Executive Summary
This document provides a comprehensive inventory and functional mapping of the KavachX codebase, confirming the separation between production runtime, native acceleration, automated testing, developer tooling, documentation, and historical validation records.

---

## 2. Directory Structure & Component Classification

| Directory | Role / Classification | Authoritative Status | Key Responsibilities |
| :--- | :--- | :---: | :--- |
| `src/kavachx/` | Production Python Package | **AUTHORITATIVE** | Ingestion pipeline, camera abstraction, IPC client, DFL box decoding, alert event management, configuration loader, service health. |
| `native/worker/` | Native C++ NPU Worker | **AUTHORITATIVE** | Qualcomm QNN HTP runtime loader, FastRPC transport (`/dev/fastrpc-cdsp`), UNIX domain socket server, zero-copy buffer execution. |
| `models/production/` | Production Artifacts | **FROZEN** | Quantized INT8 context binary (`3class_calibrated_final.bin`, SHA256: `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc`). |
| `models/reference/` | Golden Reference Artifacts | **REFERENCE** | Split FP32 ONNX model (`new_3class_best_FP32_htp_split.onnx`) used for numerical parity baseline. |
| `config/` | System Configuration | **AUTHORITATIVE** | Production runtime settings (`production.json`) and systemd daemon service descriptor (`kawach_worker.service`). |
| `deployment/` | Turnkey Lifecycle Scripts | **AUTHORITATIVE** | Automated installation (`install.sh`), uninstallation (`uninstall.sh`), and interactive demo runner (`run_demo.sh`). |
| `tests/` | Automated Regression Suites | **AUTHORITATIVE** | Hardware DSP tests (`hardware/`), pipeline integration tests (`integration/`), bounded live streaming tests (`streaming/`), and fixtures. |
| `tools/` | Developer Utilities | **UTILITIES** | Benchmarks (`benchmark.py`), environment diagnostics (`diagnostics.py`), model inspectors (`model_inspect.py`), service supervisor (`service_manager.py`), target runner (`target_runner.py`), and live camera viewer (`live_camera_viewer.py`). |
| `docs/` | Technical Documentation | **AUTHORITATIVE** | Comprehensive system architecture, model quantization, streaming, deployment, operations, testing, and audit manuals. |
| `reports/` | Frozen Validation Evidence | **EVIDENCE** | Acceptance matrices, performance records, concurrency reports, and reliability logs. |
| `archive/` | Historical Evidence | **ARCHIVE** | Historical development milestones and migration tooling preserved with zero data loss. |

---

## 3. Production Source Module Inventory

### 3.1 `src/kavachx/inference/`
- `engine.py` (`InferenceEngine`): High-level inference interface connecting frame preprocessing, IPC dispatch, and post-inference DFL decoding.
- `model.py` (`Detection`, `InferenceOutput`): Strongly typed dataclasses representing unpadded bounding boxes, confidence values, and latency metrics.
- `decoder.py` (`decode_detections`): Vectorized box decoding and confidence filtering over the $[1, 64, 8400]$ and $[1, 3, 8400]$ tensor outputs.
- `postprocess.py` (`letterbox_with_meta`, `prepare_uint8_nchw`): High-performance aspect-ratio preserving letterbox transformer yielding $[1, 3, 640, 640]$ uint8 NCHW tensors.

### 3.2 `src/kavachx/pipeline/`
- `processor.py` (`StreamProcessor`): Dual-threaded live stream coordinator orchestrating asynchronous camera ingestion and sequential NPU inference.
- `frame_queue.py` (`BoundedQueue`): Drop-tail bounded queue (`maxsize=2`) enforcing a **latest-frame-wins** policy under inference backpressure.
- `events.py` (`AlertEventManager`): Time-debounced hazard alert dispatcher generating `HAZARD_DETECTED` (Fire: Critical, Smoke: Warning) and `PERSON_DETECTED` (Person: Warning) events.

### 3.3 `src/kavachx/capture/`
- `camera.py` (`create_capture_source`): Factory creating stream ingestion adapters based on configuration.
- `v4l2.py` (`V4L2Source`): Direct capture from physical USB and CSI camera devices (`/dev/video*`).
- `rtsp.py` (`RTSPSource`): RTSP IP camera client with automatic reconnection and exponential backoff.
- `video.py` (`VideoSource`): Continuous synthetic loop and file streaming driver for validation.

### 3.4 `src/kavachx/ipc/`
- `protocol.py`: Protocol framing constants (Request Magic: `0x4B574158` / "KWAX", Response Magic: `0x5841574B` / "XAWK").
- `client.py` (`IpcClient`): Low-latency UNIX domain stream socket client communicating with the native worker daemon.

### 3.5 `src/kavachx/service/`
- `health.py` (`get_service_health`, `is_healthy`): JSON state inspector polling `/tmp/kawach_health.json`.

### 3.6 `native/worker/`
- `main.cpp`: Entry point, command-line argument parser, daemon lifecycle management, and socket server.
- `qnn_inference.cpp` / `qnn_inference.hpp`: Qualcomm QNN SDK C API loader, HTP backend initialization, context binary deserialization, and FastRPC execution.
- `ipc_handler.cpp` / `ipc_handler.hpp`: Non-blocking socket listener, request frame deserializer, and response frame encoder.
