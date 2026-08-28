# KavachX — Real-Time Hazard & Person Perception System

KavachX is an enterprise edge perception system for real-time detection of **Fire, Smoke, and Persons**, hardware-accelerated on the **Qualcomm Hexagon v68 HTP DSP** on the Qualcomm QCS6490 SoC (Radxa Dragon Q6490 / Kavach-EdgeBox).

---

## 1. Executive Summary & Verified Hardware Baseline

- **Hardware Platform:** Qualcomm QCS6490 SoC (Qualcomm Hexagon v68 HTP DSP).
- **Quantization:** Calibrated INT8 compiled QNN context binary.
- **Model Signature:** [`models/production/3class_calibrated_final.bin`](models/production/3class_calibrated_final.bin) (26.8 MB, SHA256: `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc`).
- **Hardware Acceleration:** **100% Neural Network on Hexagon DSP** via FastRPC (`/dev/fastrpc-cdsp`) with **0 CPU/GPU fallback**.
- **Performance:**
  - **Raw NPU Inference Latency:** $\sim 30.14\text{ ms}$ ($\sim 33.2\text{ FPS}$).
  - **End-to-End Live Stream Pipeline:** $\sim 61.91\text{ ms}$ ($\sim 13.9\text{ FPS}$) including capture, letterboxing, NPU execution, DFL decoding, NMS, and debounced alert dispatching.
- **Target Classes:** `fire` (CRITICAL), `smoke` (WARNING), `person` (WARNING).

---

## 2. End-to-End Pipeline Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│  Camera Ingestion Layer (src/kavachx/capture/)                         │
│  - V4L2 Physical USB/CSI Camera (/dev/video0)                          │
│  - Network RTSP IP Camera (rtsp://...)                                 │
│  - Continuous Video Stream (test_data/videos/live_test_stream.mp4)      │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Bounded Frame Queue (src/kavachx/pipeline/frame_queue.py)             │
│  - Latest-Frame-Wins drop policy (maxsize=2, prevents latency buildup) │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Preprocessing & IPC Client (src/kavachx/inference/)                   │
│  - Letterbox to [1, 3, 640, 640] uint8 NCHW                            │
│  - UNIX domain socket transfer to daemon (/tmp/kawach_worker.sock)     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼ (FastRPC /dev/fastrpc-cdsp)
┌────────────────────────────────────────────────────────────────────────┐
│  Native C++ Worker on Qualcomm Hexagon v68 HTP DSP (native/worker/)    │
│  - QNN HTP Backend (libQnnHtp.so)                                      │
│  - 100% DSP Execution (Backbone, FPN Neck, Output Convolution Heads)   │
│  - Zero CPU Fallback for neural network layers                         │
│  - Returns INT8 outputs: [1, 64, 8400] & [1, 3, 8400] uint8            │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  DFL Box Decoding & NMS (src/kavachx/inference/decoder.py)             │
│  - Vectorized expectation over 16 DFL bins per coordinate              │
│  - Unletterboxes coordinates to original camera resolution             │
│  - Extracts bounding boxes [x1, y1, x2, y2] + confidence scores        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Alert & Event Manager (src/kavachx/pipeline/events.py)                │
│  - Debounced event dispatching (cooldown = 3.0s)                       │
│  - HAZARD_DETECTED (Fire: CRITICAL, Smoke: WARNING)                    │
│  - PERSON_DETECTED (Person: WARNING)                                   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. How to Run the Application

The system can be controlled directly from your **Windows PowerShell terminal** or natively on the **Linux EdgeBox**.

### Option A: From Windows Desktop (VS Code / PowerShell)

Run commands using the target execution runner:

```powershell
# 1. Run Live Interactive Demo (Worker Health + 50 Live Stream Frames)
python tools/target_runner.py "cd /home/work_user2/kawachx_task && make demo"

# 2. Watch Real-Time Detections & Bounding Boxes Frame-by-Frame
python tools/target_runner.py "cd /home/work_user2/kawachx_task && python3 tools/live_camera_viewer.py 20"

# 3. Run Automated Regression Test Suite
python tools/target_runner.py "cd /home/work_user2/kawachx_task && make test"

# 4. Check Production Daemon Health
python tools/target_runner.py "cat /tmp/kawach_health.json"
```

---

### Option B: Directly on the Qualcomm EdgeBox (SSH)

Log into the EdgeBox:
```bash
ssh work_user2@ssh.kavachx.io
cd /home/work_user2/kawachx_task
```

Execute production commands:
```bash
# Build native C++ worker
make build

# Start the background daemon
python3 tools/service_manager.py start

# Check service health
cat /tmp/kawach_health.json

# Run live stream viewer
python3 tools/live_camera_viewer.py 20

# Run full test suite
make test
```

---

## 4. Technical Documentation Package

Complete technical documentation is organized in the [`docs/`](docs/) directory:

| Domain | Documentation File | Description |
| :--- | :--- | :--- |
| **Architecture** | [`docs/architecture/SYSTEM_ARCHITECTURE.md`](docs/architecture/SYSTEM_ARCHITECTURE.md) | High-level architecture, boundaries, and data flow. |
| | [`docs/architecture/COMPONENTS.md`](docs/architecture/COMPONENTS.md) | Component responsibilities, inputs, and outputs. |
| | [`docs/architecture/DATA_FLOW.md`](docs/architecture/DATA_FLOW.md) | End-to-end frame transformations and tensor formats. |
| | [`docs/architecture/PROCESS_AND_THREADING.md`](docs/architecture/PROCESS_AND_THREADING.md) | Multi-threading model and IPC synchronization. |
| **Model & NPU** | [`docs/model/MODEL_OVERVIEW.md`](docs/model/MODEL_OVERVIEW.md) | YOLOv8 architecture, tensor shapes, and split head design. |
| | [`docs/model/QUANTIZATION.md`](docs/model/QUANTIZATION.md) | Symmetric INT8 quantization and QNN context binary compilation. |
| | [`docs/model/HTP_ACCELERATION.md`](docs/model/HTP_ACCELERATION.md) | Qualcomm Hexagon v68 HTP DSP FastRPC execution. |
| | [`docs/model/DFL_AND_POSTPROCESSING.md`](docs/model/DFL_AND_POSTPROCESSING.md) | DFL coordinate decoding and coordinate unletterboxing. |
| | [`docs/model/NUMERICAL_VALIDATION.md`](docs/model/NUMERICAL_VALIDATION.md) | Empirical accuracy and numerical parity vs. FP32 reference. |
| **Streaming** | [`docs/streaming/STREAMING_PIPELINE.md`](docs/streaming/STREAMING_PIPELINE.md) | Bounded drop queue and latest-frame-wins drop policy. |
| | [`docs/streaming/CAMERA_INTEGRATION.md`](docs/streaming/CAMERA_INTEGRATION.md) | Physical USB/CSI (`/dev/video0`), RTSP, and Video stream setup. |
| | [`docs/streaming/IPC_PROTOCOL.md`](docs/streaming/IPC_PROTOCOL.md) | Binary framing specification (`0x4B574158` / `0x5841574B`). |
| **Deployment** | [`docs/deployment/DEPLOYMENT_GUIDE.md`](docs/deployment/DEPLOYMENT_GUIDE.md) | Turnkey installation, user permissions, and service setup. |
| | [`docs/deployment/PRODUCTION_CONFIGURATION.md`](docs/deployment/PRODUCTION_CONFIGURATION.md) | Centralized runtime configuration (`config/production.json`). |
| **Testing** | [`docs/testing/TEST_STRATEGY.md`](docs/testing/TEST_STRATEGY.md) | Multi-tier validation strategy across hardware, integration, and streaming. |
| | [`docs/testing/TESTING_AND_VALIDATION.md`](docs/testing/TESTING_AND_VALIDATION.md) | Automated regression test results and recovery verification. |
| | [`docs/testing/PERFORMANCE.md`](docs/testing/PERFORMANCE.md) | Latency, throughput, and memory characterization on hardware. |
| | [`docs/testing/RELIABILITY_AND_FAILURE_RECOVERY.md`](docs/testing/RELIABILITY_AND_FAILURE_RECOVERY.md) | Process isolation, worker self-healing, and memory stability. |
| **Operations** | [`docs/operations/OPERATIONS_RUNBOOK.md`](docs/operations/OPERATIONS_RUNBOOK.md) | Production operations manual (start, stop, restart, status, logs). |
| | [`docs/operations/HEALTH_AND_MONITORING.md`](docs/operations/HEALTH_AND_MONITORING.md) | JSON health monitoring endpoint (`/tmp/kawach_health.json`). |
| **Assignment** | [`docs/assignment/ASSIGNMENT_COVERAGE.md`](docs/assignment/ASSIGNMENT_COVERAGE.md) | 100% compliance mapping against assessment instructions. |
| | [`docs/assignment/SUBMISSION_GUIDE.md`](docs/assignment/SUBMISSION_GUIDE.md) | Evaluator quickstart guide. |
| **Audits** | [`docs/audit/REPOSITORY_AUDIT.md`](docs/audit/REPOSITORY_AUDIT.md) | Complete codebase inventory and component mapping. |
| | [`docs/audit/ASSIGNMENT_REQUIREMENTS.md`](docs/audit/ASSIGNMENT_REQUIREMENTS.md) | Extracted requirements matrix. |
| | [`docs/audit/EVIDENCE_MATRIX.md`](docs/audit/EVIDENCE_MATRIX.md) | Traceability matrix linking code, tests, and evidence. |
| | [`docs/audit/CLAIMS_AND_EVIDENCE.md`](docs/audit/CLAIMS_AND_EVIDENCE.md) | Empirical evidence supporting all performance claims. |
| | [`docs/audit/DOCUMENTATION_FINAL_AUDIT.md`](docs/audit/DOCUMENTATION_FINAL_AUDIT.md) | Final consistency and integrity audit report. |

---

## 5. Repository Structure

```text
KavachX/
├── README.md                          # Production product overview & run guide
├── LICENSE                            # Apache 2.0 License
├── Makefile                           # Target build, test, clean, demo, and health targets
├── pyproject.toml                     # Python packaging configuration
├── requirements.txt                   # Production Python dependencies
├── .gitignore                         # Build and runtime artifact filter
│
├── src/                               # Authoritative Python Production Package
│   └── kavachx/
│       ├── inference/                 # Inference engine, DFL decoder, letterbox postprocessing
│       ├── pipeline/                  # Live stream pipeline, bounded drop queue, alert events
│       ├── capture/                   # Unified camera sources (V4L2, RTSP, Video file)
│       ├── ipc/                       # Framed binary socket protocol & client
│       ├── service/                   # Health inspection & daemon state
│       ├── config/                    # Production configuration loader
│       └── common/                    # Logging and process utilities
│
├── native/                            # Production Native C++ Worker
│   └── worker/                        # Qualcomm Hexagon HTP FastRPC Zero-Copy Daemon
│       ├── main.cpp
│       ├── qnn_inference.cpp
│       ├── qnn_inference.hpp
│       ├── ipc_handler.cpp
│       ├── ipc_handler.hpp
│       └── Makefile
│
├── models/
│   ├── production/
│   │   └── 3class_calibrated_final.bin # Frozen Quantized HTP Context Binary (26.8MB)
│   └── reference/
│       └── new_3class_best_FP32_htp_split.onnx
│
├── config/
│   ├── production.json                # Authoritative production configuration
│   └── kawach_worker.service          # Systemd daemon service descriptor
│
├── deployment/                        # Turnkey Deployment Scripts
│   ├── install.sh
│   ├── uninstall.sh
│   ├── run_demo.sh
│   └── README.md
│
├── tests/                             # Automated Test Suites
│   ├── hardware/                      # test_htp_inference.py (Qualcomm DSP verification)
│   ├── integration/                   # test_pipeline_integration.py
│   ├── streaming/                     # test_live_stream.py
│   ├── unit/                          # Unit tests
│   └── fixtures/                      # Mock feeds & test inputs
│
├── tools/                             # Developer & Diagnostic Utilities
│   ├── benchmark.py                   # Hardware latency & throughput benchmark
│   ├── diagnostics.py                 # FastRPC & runtime environment health checker
│   ├── live_camera_viewer.py          # Real-time frame-by-frame detection stream viewer
│   ├── model_inspect.py               # Inspects model binary parameters & checksum
│   ├── service_manager.py             # Service supervisor (start, stop, restart, status)
│   └── target_runner.py               # Remote execution & validation driver
│
├── docs/                              # Product Technical Documentation (28+ manuals)
├── reports/                           # Archived Verification Reports
├── test_data/                         # Verification Media (images/ & videos/)
└── archive/                           # Preserved Historical Development Milestones
```

---

## 6. License
Apache License 2.0. Copyright (c) 2026 KavachX Team.