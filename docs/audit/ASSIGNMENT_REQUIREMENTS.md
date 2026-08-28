# Technical Assessment Requirements Audit

## 1. Source Document
- **Assessment Title:** Technical Assessment — On-Device NPU Deployment
- **Target Role:** AI/ML Engineer (Edge Deployment)
- **Target Hardware:** Qualcomm QCS6490 SoC (Hexagon NPU / HTP v68)
- **Problem Statement:** Deploy a 3-class object detection model (Fire, Smoke, Person) to run real-time inference on the Qualcomm NPU with zero CPU/GPU fallback.

---

## 2. Requirement Extraction Matrix

| Req ID | Core Requirement | Interpretation & Acceptance Criteria | Required Evidence |
| :---: | :--- | :--- | :--- |
| **REQ-1** | **INT8 QNN Context Binary** | Quantize and compile the FP32 source ONNX model into a valid `.bin` context binary for Qualcomm Hexagon HTP v68. | Working `.bin` file with frozen SHA256 checksum; successful deserialization via QNN HTP backend. |
| **REQ-2** | **100% NPU Hardware Execution** | Inference must execute entirely on the Hexagon NPU/HTP via FastRPC with zero CPU or GPU neural network fallback. | `/dev/fastrpc-cdsp` active; verified `libQnnHtp.so` execution; 0 CPU fallback layers. |
| **REQ-3** | **C++ `npu_worker` Integration** | Load the context binary into the C++ runtime and serve requests over the exposed IPC interface. | Native worker builds cleanly, creates UNIX domain socket, and returns valid output tensors. |
| **REQ-4** | **Numerical Parity & Validation** | Demonstrate real image inference output is numerically valid and consistent with the FP32 reference model. | Class agreement, high IoU overlap ($>0.85$), and valid bounding boxes on real imagery. |
| **REQ-5** | **End-to-End Live Integration** | Connect the NPU worker to continuous camera ingestion with real-time bounding box decoding and alerts. | Working camera/video ingestion, bounded drop queue, sub-second latency, debounced alerts. |
| **REQ-6** | **Engineering Critique & Judgment** | Document what worked, what failed, why the dynamic DFL slice blocked compilation, and critique the base architecture & IPC design. | Detailed architectural report comparing YOLOv8 DFL vs anchor-based detectors and shared memory IPC. |
| **REQ-7** | **Submission Packaging** | Professional repository layout with build scripts, runbooks, tests, and documentation. | Root `README.md`, `Makefile`, `pyproject.toml`, structured `docs/`, `tests/`, and `tools/`. |
