# End-to-End Data Flow Architecture

## 1. Data Transformations Across Subsystems

```text
1. CAMERA INGESTION:
   Raw Frame (e.g. 1920x1080 BGR) captured via V4L2 or RTSP adapter.
        │
        ▼
2. BOUNDED QUEUE:
   Frame placed in BoundedQueue(maxsize=2). If full, oldest frame is evicted.
        │
        ▼
3. PREPROCESSING:
   - Color space conversion: BGR -> RGB.
   - Aspect-preserving letterbox resizing -> 640x640 with (114,114,114) border.
   - Transpose & layout: HWC -> NCHW [1, 3, 640, 640] uint8.
   - Metadata recorded: scale factor r, horizontal padding dw, vertical padding dh.
        │
        ▼
4. BINARY IPC FRAMING:
   - 16-byte Header: Magic 0x4B574158 ("KWAX"), Sequence ID, Payload Length (1,228,800 bytes).
   - Payload: 1,228,800 bytes raw uint8 buffer.
   - Sent via UNIX domain stream socket to /tmp/kawach_worker.sock.
        │
        ▼
5. DSP HARDWARE EXECUTION:
   - Worker copies buffer to QNN input tensor memory.
   - FastRPC transfer to Hexagon v68 HTP DSP (/dev/fastrpc-cdsp).
   - 100% Neural Network execution on DSP (~30.14 ms).
   - DSP outputs:
     * output_0: [1, 64, 8400] uint8 (DFL box distribution)
     * output_1: [1, 3, 8400] uint8 (Class probabilities)
        │
        ▼
6. IPC RESPONSE:
   - 28-byte Header: Magic 0x5841574B ("XAWK"), Status (0=SUCCESS), Latency metrics.
   - Payload: 235,200 bytes raw float32 tensor [7, 8400].
        │
        ▼
7. DFL BOX DECODING & NMS (CPU: <1 ms):
   - Softmax and expectation over 16 DFL bins per coordinate.
   - Coordinate unletterbox: x = (x_lb - dw) / r, y = (y_lb - dh) / r.
   - Confidence threshold filtering (conf >= 0.25) and NMS filtering (IoU >= 0.45).
        │
        ▼
8. EVENT DISPATCH:
   - Detections mapped to event taxonomy.
   - Debouncing applied (cooldown = 3.0s).
   - Dispatched to alert sinks and monitoring endpoints.
```
