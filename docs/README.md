# KavachX — Master Technical Documentation Suite

Welcome to the technical documentation for **KavachX**, an enterprise edge perception system hardware-accelerated on the **Qualcomm Hexagon v68 HTP DSP** on the Qualcomm QCS6490 SoC.

---

## 1. Quick Navigation & Walkthrough
- [**Getting Started Guide**](GETTING_STARTED.md) — 5-minute technical orientation for new engineers.
- [**Technical Assessment & Deployment Report**](TECHNICAL_ASSESSMENT_REPORT.md) — Executive summary and reviewer-facing submission report.

---

## 2. Architecture & Design
- [**System Architecture**](architecture/SYSTEM_ARCHITECTURE.md) — High-level architecture, end-to-end dataflow, and boundary definitions.
- [**Technology Stack Specification**](architecture/TECHNOLOGY_STACK.md) — Comprehensive verified hardware, runtime, and software stack.
- [**Repository Architecture**](architecture/REPOSITORY_ARCHITECTURE.md) — Production, test, tooling, and archive classification.
- [**Process Architecture**](architecture/PROCESS_ARCHITECTURE.md) — Multi-process isolation, threads, and FastRPC lifecycle.
- [**Engineering Decisions Log**](architecture/ENGINEERING_DECISIONS.md) — Architectural trade-offs and decision rationale.
- [**Component Responsibilities**](architecture/COMPONENTS.md) — Component inputs, outputs, and failure boundaries.
- [**End-to-End Data Flow**](architecture/DATA_FLOW.md) — Frame transformations from camera capture to alert dispatch.
- [**Threading Model**](architecture/PROCESS_AND_THREADING.md) — Ingestion and inference synchronization model.

---

## 3. Machine Learning & Qualcomm NPU Acceleration
- [**Model Architecture & Tensors**](model/MODEL_ARCHITECTURE.md) — Visual YOLOv8 model flow and static tensor contracts.
- [**Model Visual Summary**](model/MODEL_SUMMARY.md) — Quick reference properties and checksums.
- [**Graph Splitting Rationale**](model/GRAPH_SPLITTING.md) — Resolution of the dynamic DFL slice compiler blocker.
- [**HTP vs. CPU Execution Boundary**](model/HTP_EXECUTION.md) — Visual breakdown of DSP neural execution vs. host CPU math.
- [**INT8 Quantization & Calibration**](model/QUANTIZATION.md) — Symmetric INT8 calibration and QNN context generation.
- [**Qualcomm Hexagon HTP Acceleration**](model/HTP_ACCELERATION.md) — FastRPC transport (`/dev/fastrpc-cdsp`) and zero CPU fallback.
- [**DFL Coordinate Decoding**](model/DFL_AND_POSTPROCESSING.md) — Vectorized coordinate expectation and unletterbox scaling.
- [**Numerical Parity Validation**](model/NUMERICAL_VALIDATION.md) — Empirical accuracy parity against FP32 reference (100% Top-1, 0.912 IoU).

---

## 4. Native Runtime & IPC
- [**Native C++ Worker Daemon**](runtime/NATIVE_RUNTIME.md) — FastRPC context manager and socket listener.
- [**Binary IPC Protocol**](runtime/IPC_ARCHITECTURE.md) — Binary socket framing specification (`0x4B574158` / `0x5841574B`).

---

## 5. Real-Time Streaming & Ingestion
- [**Camera Ingestion Architecture**](streaming/CAMERA_ARCHITECTURE.md) — V4L2 USB/CSI, RTSP IP camera, and video file adapters.
- [**Complete Frame Lifecycle**](streaming/FRAME_LIFECYCLE.md) — Sequence diagram from camera frame to alert dispatch.
- [**Bounded Queue & Drop Policy**](streaming/FRAME_QUEUE.md) — Bounded queue (`maxsize=2`) and latest-frame-wins drop policy.
- [**Alert Event Pipeline**](streaming/EVENT_PIPELINE.md) — Debounced hazard classification and event taxonomy.
- [**Streaming Pipeline Manual**](streaming/STREAMING_PIPELINE.md) — Dual-threaded live stream coordination.
- [**Camera Setup Guide**](streaming/CAMERA_INTEGRATION.md) — Hardware camera configuration parameters.
- [**IPC Protocol Framing**](streaming/IPC_PROTOCOL.md) — Binary framing wire specification.

---

## 6. Turnkey Deployment & Operations
- [**Deployment Architecture**](deployment/DEPLOYMENT_ARCHITECTURE.md) — Host-to-target deployment and runtime layout.
- [**Turnkey Deployment Guide**](deployment/DEPLOYMENT_GUIDE.md) — Installation, permissions (GID 993 render), and initialization.
- [**Production Configuration**](deployment/PRODUCTION_CONFIGURATION.md) — Centralized runtime reference (`config/production.json`).
- [**Service Lifecycle & State Machine**](operations/SERVICE_LIFECYCLE.md) — Supervisor state transitions and self-healing.
- [**Production Operations Runbook**](operations/OPERATIONS_RUNBOOK.md) — Standard operating procedures (start, stop, restart, status, logs).
- [**Health & Monitoring**](operations/HEALTH_AND_MONITORING.md) — JSON health monitoring endpoint (`/tmp/kawach_health.json`).

---

## 7. Testing, Performance & Security
- [**Test Architecture**](testing/TEST_ARCHITECTURE.md) — Multi-tier test map across hardware, integration, and streaming.
- [**Empirical Performance Characterization**](testing/PERFORMANCE.md) — Measured latencies (30.14 ms NPU, 61.91 ms Full Pipeline).
- [**Failure Recovery Specification**](testing/FAILURE_RECOVERY.md) — Fault-tolerance matrix and auto-recovery flow.
- [**Test Strategy**](testing/TEST_STRATEGY.md) — Test methodology and verification principles.
- [**Testing & Validation Results**](testing/TESTING_AND_VALIDATION.md) — Automated regression test results.
- [**Security Architecture & Controls**](security/SECURITY_ARCHITECTURE.md) — Resource bounds, isolation, and access controls.

---

## 8. Assignment Traceability & Audits
- [**Requirements Traceability Matrix**](assignment/REQUIREMENT_TRACEABILITY.md) — Traces every assessment requirement to source code and tests.
- [**Assignment Coverage Report**](assignment/ASSIGNMENT_COVERAGE.md) — 100% compliance mapping against assessment instructions.
- [**Evaluator Submission Guide**](assignment/SUBMISSION_GUIDE.md) — Evaluator quickstart runbook.
- [**Repository Audit**](audit/REPOSITORY_AUDIT.md) — Complete codebase inventory and component mapping.
- [**Assignment Requirements Audit**](audit/ASSIGNMENT_REQUIREMENTS.md) — Extracted requirements matrix.
- [**Evidence Matrix**](audit/EVIDENCE_MATRIX.md) — Evidence tracing matrix.
- [**Claims & Evidence Registry**](audit/CLAIMS_AND_EVIDENCE.md) — Empirical evidence supporting all performance claims.
- [**Documentation Final Audit**](audit/DOCUMENTATION_FINAL_AUDIT.md) — Consistency and integrity audit report.
