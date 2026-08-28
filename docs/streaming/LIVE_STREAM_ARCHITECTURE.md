# Live Stream Pipeline Architecture

## 1. Dual-Threaded Stream Coordinator
`src/kavachx/pipeline/processor.py` orchestrates frame ingestion and inference across two independent threads:

```text
[ Camera Ingestion Thread ] ---> [ BoundedQueue (maxsize=2) ] ---> [ Inference Thread ]
  - Captures at camera rate        - Latest-frame-wins              - FastRPC NPU inference
  - Handles reconnects             - Drops stale frames             - DFL & NMS decode
```
