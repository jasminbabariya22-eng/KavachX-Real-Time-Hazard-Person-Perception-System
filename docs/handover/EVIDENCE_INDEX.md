# Technical Evidence & Reproducibility Index

## 1. Empirical Evidence Tracing

| Technical Claim | Verified Value | Evidence File / Artifact | Exact Verification Command |
| :--- | :--- | :--- | :--- |
| **100% HTP Execution** | 0 CPU Fallback Layers | `tests/hardware/test_htp_inference.py` | `make test` |
| **Raw DSP Latency** | 30.14 ms Mean, 32.40 ms P95 | `tools/benchmark.py` | `python3 tools/benchmark.py` |
| **Live Stream Latency** | 61.91 ms Mean (13.9 FPS) | `tests/streaming/test_live_stream.py` | `make demo` |
| **Numerical Parity** | 100% Class match, 0.912 IoU | `docs/model/MODEL_VALIDATION.md` | Evaluated on `data/test_images/` |
| **Model Integrity** | SHA256 Checksum Match | `models/production/3class_calibrated_final.bin` | `python3 tools/model_inspect.py` |
| **Worker Self-Healing**| Auto-Restart on Crash | `tools/service_manager.py` | `python3 tools/service_manager.py restart` |
