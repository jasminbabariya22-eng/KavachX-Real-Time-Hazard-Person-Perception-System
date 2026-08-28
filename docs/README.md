# KavachX Technical Documentation

Welcome to the technical documentation for **KavachX**, an enterprise edge computer vision system hardware-accelerated on the **Qualcomm Hexagon v68 HTP DSP**.

---

## 1. System Architecture & Design
- [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) — Comprehensive architecture, dataflow, and boundary definitions.
- [System Components](architecture/COMPONENTS.md) — Component responsibilities, inputs, outputs, and lifecycle.
- [End-to-End Data Flow](architecture/DATA_FLOW.md) — Detailed frame lifecycle and tensor transformations.
- [Process & Threading Model](architecture/PROCESS_AND_THREADING.md) — Multi-threading and IPC synchronization model.

## 2. Model & NPU Acceleration
- [Model Overview](model/MODEL_OVERVIEW.md) — YOLOv8 architecture, classes, and split graph design.
- [Quantization & Compilation](model/QUANTIZATION.md) — INT8 quantization process and QNN context binary compilation.
- [Qualcomm HTP Acceleration](model/HTP_ACCELERATION.md) — FastRPC transport and zero CPU fallback architecture.
- [DFL Decoding & Postprocessing](model/DFL_AND_POSTPROCESSING.md) — Vectorized box decoding and coordinate unletterboxing.
- [Numerical Parity Validation](model/NUMERICAL_VALIDATION.md) — Empirical accuracy parity against FP32 golden reference.

## 3. Streaming & Ingestion
- [Streaming Pipeline](streaming/STREAMING_PIPELINE.md) — Bounded drop queue and latest-frame-wins drop policy.
- [Camera Integration Guide](streaming/CAMERA_INTEGRATION.md) — V4L2 USB/CSI, RTSP IP stream, and video file setup.
- [Binary IPC Protocol](streaming/IPC_PROTOCOL.md) — Binary socket framing specification (`0x4B574158` / `0x5841574B`).

## 4. Deployment & Configuration
- [Turnkey Deployment Guide](deployment/DEPLOYMENT_GUIDE.md) — Installation, permissions, and service initialization.
- [Production Configuration](deployment/PRODUCTION_CONFIGURATION.md) — Centralized configuration reference (`config/production.json`).

## 5. Testing, Reliability & Performance
- [Test Strategy](testing/TEST_STRATEGY.md) — Multi-tier testing approach across hardware, integration, and streaming.
- [Testing & Validation Results](testing/TESTING_AND_VALIDATION.md) — Automated regression and failure-recovery results.
- [Performance Characterization](testing/PERFORMANCE.md) — Raw NPU latency vs. full pipeline streaming latency.
- [Reliability & Failure Recovery](testing/RELIABILITY_AND_FAILURE_RECOVERY.md) — Fault tolerance, watchdog recovery, and stability.

## 6. Operations & Monitoring
- [Operations Runbook](operations/OPERATIONS_RUNBOOK.md) — Standard operating procedures (start, stop, restart, status).
- [Health & Monitoring](operations/HEALTH_AND_MONITORING.md) — Real-time health reporting specification (`/tmp/kawach_health.json`).

## 7. Assignment Coverage & Evaluator Guide
- [Assignment Coverage](assignment/ASSIGNMENT_COVERAGE.md) — Detailed mapping of assessment criteria to deliverables.
- [Submission & Evaluator Guide](assignment/SUBMISSION_GUIDE.md) — Quickstart evaluation runbook.

## 8. Audits & Evidence Registries
- [Repository Audit](audit/REPOSITORY_AUDIT.md) — Full repository inventory and classification.
- [Assignment Requirements](audit/ASSIGNMENT_REQUIREMENTS.md) — Extracted requirements matrix.
- [Evidence Matrix](audit/EVIDENCE_MATRIX.md) — Traceability matrix linking code, tests, and evidence.
- [Claims & Evidence Registry](audit/CLAIMS_AND_EVIDENCE.md) — Empirical evidence supporting all performance claims.
- [Documentation Final Audit](audit/DOCUMENTATION_FINAL_AUDIT.md) — Consistency and integrity audit report.
