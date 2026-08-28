# Testing & Validation Results

## 1. Automated Regression Results

| Test Suite | Purpose | Target Hardware | Result |
| :--- | :--- | :--- | :---: |
| `tests/hardware/test_htp_inference.py` | Direct FastRPC NPU communication & DSP tensor validation. | Qualcomm Hexagon v68 DSP | **PASS** |
| `tests/integration/test_pipeline_integration.py` | Aspect-preserving letterbox, bounded queue, DFL decode. | Kryo 670 CPU + Hexagon DSP | **PASS** |
| `tests/streaming/test_live_stream.py` | Continuous live stream throughput (40 frames). | Qualcomm QCS6490 SoC | **PASS** |
| `tools/service_manager.py` | Supervisor lifecycle, pre-flight checks, auto-restart. | Linux system daemon | **PASS** |

---

## 2. Fault-Tolerance & Recovery Matrix

| Scenario | Tested Condition | System Behavior | Result |
| :--- | :--- | :--- | :---: |
| **Camera Disconnect** | Stream drops unexpectedly | Detects disconnect, triggers exponential backoff reconnect; worker unaffected. | **PASS** |
| **Worker Crash** | Daemon killed via `SIGKILL` | Supervisor detects dead process, relaunches worker, re-establishes FastRPC. | **PASS** |
| **Oversized Request** | Client sends $>2	ext{ MB}$ payload | Worker returns status `1` (REJECTED) without crashing. | **PASS** |
| **Truncated Request** | Incomplete packet sent | Worker closes broken connection safely; accepts next client request. | **PASS** |
| **Frame Overload** | Ingestion FPS > DSP throughput | Bounded queue evicts oldest frame; zero backlog accumulation. | **PASS** |
