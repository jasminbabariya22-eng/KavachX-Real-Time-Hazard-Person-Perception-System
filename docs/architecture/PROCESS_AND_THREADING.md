# Process & Threading Model

## 1. Process Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│  Host Operating System (Linux 6.6 ARM64 - Qualcomm QCS6490)            │
├───────────────────────────────────┬────────────────────────────────────┤
│  Process 1: Python Stream Engine  │  Process 2: Native Worker Daemon   │
│  (src/kavachx/pipeline)           │  (native/worker/kawach_worker)     │
│                                   │                                    │
│  Thread 1: Capture Loop           │  Thread 1: Socket Acceptor Loop    │
│  Thread 2: Inference & Postproc   │  Thread 2: FastRPC HTP Worker      │
│  Thread 3: Health Monitor         │                                    │
└─────────────────┬─────────────────┴──────────────────┬─────────────────┘
                  │                                    │
                  └───────── UNIX Socket ──────────────┘
                    (/tmp/kawach_worker.sock)
```

---

## 2. Thread Safety & Synchronization

1. **Capture Thread (`_cap_loop`):**
   - Polls camera source at target FPS (e.g. $30	ext{ FPS}$).
   - Pushes frames to `BoundedQueue`. Never blocks; drops stale frames if the queue is full.
2. **Inference Thread (`_infer_loop`):**
   - Pops frames from `BoundedQueue` with a $100	ext{ ms}$ timeout.
   - Executes synchronous IPC request to `kawach_worker`.
   - Performs DFL decoding and event dispatching.
3. **C++ Socket Acceptor Thread:**
   - Listens on `/tmp/kawach_worker.sock`.
   - Handles incoming connections sequentially.
   - Validates request headers and packet lengths before processing.
