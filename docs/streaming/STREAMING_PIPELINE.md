# Real-Time Streaming Pipeline

## 1. Ingestion Architecture
The streaming engine (`src/kavachx/pipeline/processor.py`) decouples camera frame ingestion from NPU hardware inference using an asynchronous dual-thread model with a bounded queue:

```text
[ Camera Ingestion Thread ] ---> [ BoundedQueue(maxsize=2) ] ---> [ Inference Thread ]
  - Captures at camera rate        - Latest-frame-wins             - Sends to NPU
  - Handles reconnects             - Evicts stale frames           - Decodes & Alerts
```

---

## 2. Bounded Queue & Latest-Frame Policy
To prevent memory buildup and ensure sub-second operator latency when camera capture exceeds NPU inference throughput:
- Queue capacity is strictly bounded (`maxsize=2`).
- If an inference step is active when a new frame arrives, the oldest unprocessed frame is dropped immediately.
- Queue backlog growth: **0 frames**.

---

## 3. Hazard Alert Debouncing
To prevent notification storms from persistent objects:
- An alert cooldown window (`cooldown_seconds = 3.0`) is enforced per class.
- Subsequent detections of the same category within the cooldown window update the tracking state without triggering duplicate alarm dispatches.
