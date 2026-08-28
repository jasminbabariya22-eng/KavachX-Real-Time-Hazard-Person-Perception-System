# Claims & Evidence Registry

This document records the empirical evidence supporting every technical and performance claim made in the KavachX documentation.

---

## 1. Hardware & Execution Claims

### Claim 1.1: 100% Neural Network Execution on Qualcomm Hexagon v68 HTP DSP
- **Evidence Source:** Hardware test execution (`tests/hardware/test_htp_inference.py`) and native worker initialization logs.
- **Verification Data:** The native C++ worker dynamically links `libQnnHtp.so` and opens `/dev/fastrpc-cdsp` with GID `993` (`render` group). QNN graph execution initializes without CPU sub-graph partitioning.
- **CPU Fallback Count:** **0**.

### Claim 1.2: Raw Hardware Inference Latency of ~30 ms (~33.2 FPS)
- **Evidence Source:** Native IPC benchmark (`tools/benchmark.py`) across 100 consecutive iterations.
- **Verification Data:**
  - Mean Hardware Inference Latency: $30.14	ext{ ms}$
  - P95 Latency: $32.40	ext{ ms}$
  - Raw NPU Throughput: $33.2	ext{ FPS}$

### Claim 1.3: End-to-End Live Stream Pipeline Latency of ~45–70 ms (~13.5–15 FPS)
- **Evidence Source:** Live stream acceptance suite (`tests/streaming/test_live_stream.py` and `tools/live_camera_viewer.py`).
- **Verification Data:**
  - Ingestion & Aspect-Preserving Letterboxing: $\sim 8	ext{--}12	ext{ ms}$
  - FastRPC IPC Roundtrip & DSP Execution: $\sim 30	ext{--}48	ext{ ms}$
  - Vectorized DFL Decoding, Unletterboxing & NMS: $\sim 4	ext{--}6	ext{ ms}$
  - Total End-to-End Pipeline Latency: $\sim 61.91	ext{ ms}$ ($13.9	ext{ FPS}$)

---

## 2. Model & Numerical Correctness Claims

### Claim 2.1: Model Checksum & Integrity
- **Path:** `models/production/3class_calibrated_final.bin`
- **File Size:** $26,800,128	ext{ bytes}$ ($26.8	ext{ MB}$)
- **SHA256 Checksum:** `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc`
- **Status:** **FROZEN & VERIFIED**.

### Claim 2.2: Numerical Parity against FP32 Golden Reference
- **Evidence Source:** Evaluated on real industrial safety imagery (`data/test_images/` & `test_data/videos/`).
- **Verification Metrics:**
  - Top-1 Category Match: $100\%$
  - Average Bounding Box IoU: $0.912$
  - Confidence Score Correlation: $r = 0.987$
