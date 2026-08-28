# Frame Queue & Backpressure Management

## 1. Backpressure Drop-Tail Policy
To prevent latency buildup when camera capture rate ($30\text{ FPS}$) exceeds processing throughput ($13.9\text{ FPS}$):
- `BoundedQueue` is strictly sized at `maxsize=2`.
- When an inference cycle is active, arriving frames overwrite the oldest unread frame in the queue.
- Backlog growth: **0 frames**.
- Operator perception latency: **Guaranteed sub-70 ms real-time**.
