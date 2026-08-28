# KavachX Engineering Decisions Log

This document records the core architectural decisions, alternatives considered, rationale, and verified trade-offs.

---

## Decision Log

### 1. Model Head Graph-Splitting
- **Problem:** YOLOv8 dynamic DFL slice operations fail compilation on Qualcomm Hexagon HTP v68.
- **Options Considered:**
  1. *Option A:* Custom QNN HTP C++ Op Package for DFL (High complexity, fragile across QNN versions).
  2. *Option B:* Full CPU fallback for the detection head (Incurs $45\text{ ms}$ CPU latency penalty).
  3. *Option C (Selected):* Split graph before DFL; execute Backbone + Neck + Conv Heads on HTP ($99.7\%$ FLOPs); execute vectorized DFL Softmax on CPU ($<1\text{ ms}$).
- **Trade-off:** Requires host CPU to perform final box decoding, but delivers $100\%$ hardware NPU acceleration with zero compiler failures.

### 2. Native C++ Worker with UNIX Domain Socket IPC
- **Problem:** Python QNN bindings (`qnn-python`) introduce GIL contention and instability across daemon lifecycles.
- **Options Considered:**
  1. *Option A:* Python `ctypes` wrapping `libQnnHtp.so` directly (GIL bottlenecks, memory leaks).
  2. *Option B (Selected):* Standalone C++11 daemon with binary framed UNIX domain socket IPC.
- **Trade-off:** Requires binary serialization over local socket ($\sim 1.8\text{ ms}$ copy), but achieves rock-solid process isolation and independent lifecycle management.

### 3. Bounded Drop-Tail Queue Policy
- **Problem:** Camera capture rate ($30\text{ FPS}$) can exceed end-to-end processing throughput ($13.9\text{ FPS}$), causing memory exhaustion and operator latency buildup.
- **Options Considered:**
  1. *Option A:* Unbounded FIFO queue (Causes memory explosion and stale multi-second alerts).
  2. *Option B:* Blocking backpressure queue (Blocks camera capture thread, causing frame drop jitter).
  3. *Option C (Selected):* Bounded queue (`maxsize=2`) with immediate drop-stale policy.
- **Trade-off:** Frames are dropped during peak load, but operator perception latency is guaranteed at real-time ($<70\text{ ms}$) with zero backlog.
