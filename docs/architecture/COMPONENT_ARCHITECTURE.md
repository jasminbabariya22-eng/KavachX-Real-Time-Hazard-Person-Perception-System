# Component Architecture & Responsibilities

## 1. Subsystem Decomposition

| Component | Implementation File | Primary Responsibilities | Failure Isolation Boundary |
| :--- | :--- | :--- | :--- |
| **`InferenceEngine`** | `src/kavachx/inference/engine.py` | Orchestrates preprocessing, IPC socket transmission, and post-inference decoding. | Throws catchable Python exceptions; does not crash daemon. |
| **`StreamProcessor`** | `src/kavachx/pipeline/processor.py` | Dual-threaded capture and inference loop manager. | Catches stream errors and attempts auto-reconnection. |
| **`BoundedQueue`** | `src/kavachx/pipeline/frame_queue.py` | Bounded drop-tail queue enforcing a latest-frame-wins policy. | Prevents memory growth and eliminates frame latency buildup. |
| **`AlertEventManager`**| `src/kavachx/pipeline/events.py` | Time-debounced hazard alert classifier. | In-memory sliding window; safe fallback on state resets. |
| **`CameraSource`** | `src/kavachx/capture/` | Abstracted capture adapter for V4L2, RTSP, and Video feeds. | Returns `(False, None)` on disconnect; triggers reconnect loop. |
| **`IpcClient`** | `src/kavachx/ipc/client.py` | Framed binary protocol client over UNIX domain socket. | Reconnects automatically on socket closure. |
| **`kawach_worker`** | `native/worker/main.cpp` | Standalone C++11 daemon managing QNN HTP context binary. | Rejects oversized payloads ($>2\text{ MB}$) without crashing. |
| **`ServiceSupervisor`**| `tools/service_manager.py` | Lifecycle supervisor executing pre-flight checks and watchdog restarts. | Kills stale workers, restarts crashed daemons, writes health file. |
