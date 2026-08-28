# KavachX System Components

## 1. Component Responsibility Matrix

| Component | Directory | Language | Primary Responsibility | Failure Isolation |
| :--- | :--- | :---: | :--- | :--- |
| **`InferenceEngine`** | `src/kavachx/inference/engine.py` | Python | Coordinates frame preparation, IPC dispatch, and post-inference decoding. | Throws catchable Python exceptions; does not terminate worker. |
| **`StreamProcessor`** | `src/kavachx/pipeline/processor.py` | Python | Dual-threaded capture and inference loop manager. | Auto-reconnects on stream drops; catches pipeline errors. |
| **`BoundedQueue`** | `src/kavachx/pipeline/frame_queue.py` | Python | Enforces latest-frame-wins drop policy under backpressure. | Drops oldest frame if full; prevents memory growth. |
| **`AlertEventManager`** | `src/kavachx/pipeline/events.py` | Python | Debounces detections to prevent notification storms. | In-memory sliding window; safe fallback. |
| **`CameraSource`** | `src/kavachx/capture/` | Python | Abstracted capture for V4L2, RTSP, and Video feeds. | Returns `(False, None)` on disconnect; triggers reconnect loop. |
| **`IpcClient`** | `src/kavachx/ipc/client.py` | Python | Framed binary client over `/tmp/kawach_worker.sock`. | Reconnects automatically on socket closure. |
| **`kawach_worker`** | `native/worker/` | C++11 | High-performance FastRPC daemon loading QNN context binary. | Validates request sizes ($<2	ext{ MB}$); rejects malformed requests gracefully. |
| **`ServiceSupervisor`** | `tools/service_manager.py` | Python | Lifecycle manager executing pre-flight checks and daemon startup. | Kills stale workers, restarts crashed processes, writes health file. |

---

## 2. Inter-Component Communication

```text
[Camera Source] --(raw frame)--> [Stream Processor]
                                        │
                                (letterboxed tensor)
                                        │
                                        ▼
                                  [IpcClient]
                                        │
                         (UNIX Socket: /tmp/kawach_worker.sock)
                                        │
                                        ▼
                                [kawach_worker C++]
                                        │
                           (FastRPC: /dev/fastrpc-cdsp)
                                        │
                                        ▼
                           [Qualcomm Hexagon HTP DSP]
```
