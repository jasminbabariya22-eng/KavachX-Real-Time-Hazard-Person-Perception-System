# Evidence & Verification Matrix

## 1. Assignment Requirements Tracing

| Requirement ID | Requirement Description | Implementation Location | Test & Evidence Location | Status | Verified Details |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **REQ-1** | INT8 QNN Context Binary | `models/production/3class_calibrated_final.bin` | `tools/model_inspect.py`, `reports/acceptance/` | **VERIFIED** | 26.8 MB binary; SHA256 `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc`. |
| **REQ-2** | 100% NPU Hardware Execution | `native/worker/qnn_inference.cpp` | `tests/hardware/test_htp_inference.py` | **VERIFIED** | Direct FastRPC `/dev/fastrpc-cdsp` session, libQnnHtp.so active, **0 CPU fallback**. |
| **REQ-3** | C++ Worker Runtime | `native/worker/` | `native/worker/Makefile`, `tools/service_manager.py` | **VERIFIED** | Built with `g++` on ARM64; binary framing `0x4B574158` / `0x5841574B`; state `READY`. |
| **REQ-4** | Numerical Parity vs FP32 | `src/kavachx/inference/decoder.py` | `docs/model/NUMERICAL_VALIDATION.md` | **VERIFIED** | Top-1 class parity $100\%$, Mean Box IoU overlap $0.912 \pm 0.04$ on test imagery. |
| **REQ-5** | Live Streaming & Alerts | `src/kavachx/pipeline/` | `tests/streaming/test_live_stream.py`, `tools/live_camera_viewer.py` | **VERIFIED** | $13.9	ext{ FPS}$ sustained stream; debounced `HAZARD_DETECTED` and `PERSON_DETECTED` events. |
| **REQ-6** | Engineering Critique | `docs/architecture/`, `docs/model/` | `docs/handover/PRODUCTION_HANDOVER.md` | **VERIFIED** | Full diagnosis of dynamic DFL slice op, YOLOv5/v7 comparison, POSIX SHM IPC critique. |
| **REQ-7** | Production Packaging | Entire repository | Root `README.md`, `Makefile`, `pyproject.toml` | **VERIFIED** | Clean layout, zero step/phase naming in production source, verified execution. |
