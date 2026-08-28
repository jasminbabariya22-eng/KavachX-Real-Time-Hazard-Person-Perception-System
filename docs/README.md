# KavachX — Master Technical Documentation Suite

Welcome to the technical documentation portal for **KavachX**, an enterprise edge perception system hardware-accelerated on the **Qualcomm Hexagon v68 HTP DSP** on the Qualcomm QCS6490 SoC.

---

## 1. Quick Navigation & Walkthrough
- [**FULL COMPLETE PROJECT DOCUMENTATION (All-in-One Markdown)**](FULL_PROJECT_DOCUMENTATION.md) — Exhaustive monolithic technical documentation containing every single diagram, tensor specification, architecture, benchmark, and runbook.
- [**Getting Started Guide**](GETTING_STARTED.md) — 5-minute technical orientation for new engineers.
- [**Technical Assessment & Deployment Report**](TECHNICAL_ASSESSMENT_REPORT.md) — Reviewer-facing comprehensive assessment report.

---

## 2. Architecture & System Design
- [**System Overview**](architecture/SYSTEM_OVERVIEW.md) — Complete system architecture, dataflow, and boundaries.
- [**Component Architecture**](architecture/COMPONENT_ARCHITECTURE.md) — Component responsibilities, inputs, and outputs.
- [**End-to-End Data Flow**](architecture/DATA_FLOW.md) — Frame transformations from camera capture to alert dispatch.
- [**Runtime Architecture**](architecture/RUNTIME_ARCHITECTURE.md) — Python $\to$ IPC $\to$ C++ $\to$ QNN $\to$ HTP execution path.
- [**Technology Stack Specification**](architecture/TECHNOLOGY_STACK.md) — Comprehensive verified hardware, runtime, and software stack.
- [**Process Architecture**](architecture/PROCESS_ARCHITECTURE.md) — Multi-process layout, threads, and memory isolation.
- [**Engineering Decisions Log**](architecture/ENGINEERING_DECISIONS.md) — Architectural trade-offs and decision rationale.

---

## 3. Machine Learning & Qualcomm NPU Acceleration
- [**Model Overview & Specifications**](model/MODEL_OVERVIEW.md) — YOLOv8 architecture, classes, and tensor dimensions.
- [**Model Architecture & Tensors**](model/MODEL_ARCHITECTURE.md) — Visual YOLOv8 tensor flow and static input/output contracts.
- [**Model Quantization & Calibration**](model/MODEL_QUANTIZATION.md) — Symmetric INT8 quantization and QNN context binary compilation.
- [**Numerical Parity Validation**](model/MODEL_VALIDATION.md) — Accuracy parity vs. FP32 golden reference (100% Top-1, 0.912 IoU).
- [**DFL Coordinate Decoding**](model/DFL_AND_POSTPROCESSING.md) — Vectorized coordinate expectation and unletterbox scaling.
- [**Graph Splitting Rationale**](model/GRAPH_SPLITTING.md) — Resolution of the dynamic DFL slice compiler blocker.
- [**HTP vs. CPU Execution Boundary**](model/HTP_EXECUTION.md) — Visual boundary separating DSP neural operations from CPU math.

---

## 4. Native Runtime & IPC
- [**Qualcomm Hexagon HTP Runtime**](runtime/HTP_RUNTIME.md) — FastRPC transport (`/dev/fastrpc-cdsp`) and zero CPU fallback.
- [**QNN SDK C API Integration**](runtime/QNN_INTEGRATION.md) — Context deserialization and memory management.
- [**Native C++ Worker Daemon**](runtime/NATIVE_WORKER.md) — FastRPC context manager and socket listener.
- [**Binary IPC Protocol**](runtime/IPC_PROTOCOL.md) — Binary socket framing specification (`0x4B574158` / `0x5841574B`).
- [**Process Lifecycle & State Machine**](runtime/PROCESS_LIFECYCLE.md) — Supervisor state transitions and self-healing.

---

## 5. Real-Time Streaming & Ingestion
- [**Live Stream Pipeline Architecture**](streaming/LIVE_STREAM_ARCHITECTURE.md) — Dual-threaded live stream coordination.
- [**Camera Ingestion Architecture**](streaming/CAMERA_ARCHITECTURE.md) — V4L2 USB/CSI, RTSP IP stream, and Video file adapters.
- [**Frame Queue & Backpressure**](streaming/FRAME_QUEUE_AND_BACKPRESSURE.md) — Bounded queue (`maxsize=2`) and drop-tail policy.
- [**Complete Frame Lifecycle**](streaming/FRAME_LIFECYCLE.md) — Sequence diagram from camera frame to alert dispatch.
- [**Alert Event Pipeline**](streaming/EVENT_PIPELINE.md) — Debounced hazard classification and event taxonomy.
- [**Camera Integration Guide**](streaming/CAMERA_INTEGRATION.md) — Hardware camera configuration parameters.

---

## 6. Turnkey Deployment & Operations
- [**Turnkey Deployment Guide**](deployment/DEPLOYMENT_GUIDE.md) — Installation, permissions (GID 993 render), and initialization.
- [**Production Configuration Reference**](deployment/CONFIGURATION.md) — Centralized runtime reference (`config/production.json`).
- [**Go-Live & Commissioning Guide**](deployment/GO_LIVE_GUIDE.md) — Pre-commissioning checklist and verification runbook.
- [**Deployment Architecture**](deployment/DEPLOYMENT_ARCHITECTURE.md) — Host-to-target deployment flow.
- [**Production Operations Runbook**](operations/OPERATIONS_RUNBOOK.md) — Standard operating procedures (start, stop, restart, status, logs).
- [**Health & Monitoring**](operations/HEALTH_AND_MONITORING.md) — JSON health monitoring endpoint (`/tmp/kawach_health.json`).
- [**Troubleshooting Guide**](operations/TROUBLESHOOTING.md) — Diagnostic checklists and error resolution.
- [**Incident Recovery Procedures**](operations/INCIDENT_RECOVERY.md) — Automated self-healing and recovery runbooks.

---

## 7. Testing, Performance & Security
- [**Test Strategy**](testing/TEST_STRATEGY.md) — Multi-tier test methodology across hardware, integration, and streaming.
- [**Model Testing**](testing/MODEL_TESTING.md) — Quantization and numerical parity test suites.
- [**Hardware Testing**](testing/HARDWARE_TESTING.md) — FastRPC DSP execution tests.
- [**Streaming Testing**](testing/STREAMING_TESTING.md) — Continuous live stream throughput tests.
- [**Performance Characterization**](testing/PERFORMANCE_TESTING.md) — Measured latencies (30.14 ms NPU, 61.91 ms Full Pipeline).
- [**Failure Recovery Specification**](testing/FAILURE_RECOVERY.md) — Fault-tolerance matrix and auto-recovery flow.
- [**Security Architecture & Controls**](security/SECURITY_ARCHITECTURE.md) — Resource bounds, isolation, and access controls.
- [**Model Integrity & Checksum**](security/MODEL_INTEGRITY.md) — SHA256 verification and tamper protection.

---

## 8. Development & Handover
- [**Developer Onboarding Guide**](development/DEVELOPMENT_GUIDE.md) — Local development and build workflow.
- [**Repository Architecture**](development/REPOSITORY_STRUCTURE.md) — Production, test, tooling, and archive mapping.
- [**Contributing Guidelines**](development/CONTRIBUTING.md) — Code style and PR workflow.
- [**Production Handover**](handover/PRODUCTION_HANDOVER.md) — Deployment acceptance and handover specifications.
- [**Project Operational Status**](handover/PROJECT_STATUS.md) — Operational baseline and hardware verification.
- [**Technical Assessment Mapping**](handover/TECHNICAL_ASSESSMENT_MAPPING.md) — 100% compliance mapping against assessment instructions.
- [**Technical Evidence Index**](handover/EVIDENCE_INDEX.md) — Traceability registry connecting claims to empirical hardware evidence.
- [**Documentation Final Audit**](handover/DOCUMENTATION_AUDIT.md) — Final quality and consistency audit report.
