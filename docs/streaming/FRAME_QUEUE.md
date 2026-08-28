# Bounded Queue & Drop-Tail Policy

## 1. Queue Architecture Under Backpressure

```mermaid
flowchart LR
    CAM["Camera Stream (30 FPS)"] -->|Produces Frame| Q_IN["BoundedQueue\n(maxsize=2)"]
    
    subgraph QUEUE_STATE["Queue State"]
        F1["Slot 1: Current Frame"]
        F2["Slot 2: Incoming Frame"]
        DROP["[STALE FRAME EVICTED]\nZero Latency Buildup"]
    end
    
    Q_IN --> QUEUE_STATE
    QUEUE_STATE -->|Consumes Latest| INF["NPU Inference Engine (13.9 FPS)"]
```

---

## 2. Why Unbounded Queues Are Dangerous in Edge Vision
In industrial edge safety monitoring, if ingestion throughput ($30\text{ FPS}$) exceeds processing capacity ($13.9\text{ FPS}$), an unbounded queue will buffer frames. Within 60 seconds, an operator would be viewing fire alerts that occurred 30 seconds in the past, and device RAM would exhaust. The **`BoundedQueue` (maxsize=2)** guarantees that the perception engine always processes the **freshest available frame** with sub-$70\text{ ms}$ real-time latency.
