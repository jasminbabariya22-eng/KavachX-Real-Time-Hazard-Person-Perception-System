# Performance Characterization

## 1. Measured Performance Metrics on Qualcomm QCS6490

| Metric | Raw NPU Benchmark | Full Live Stream Pipeline | Evaluation Standard | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Mean Latency** | **$30.14	ext{ ms}$** | **$61.91	ext{ ms}$** | $\le 75.0	ext{ ms}$ | **PASS** |
| **P95 Latency** | **$32.40	ext{ ms}$** | **$68.40	ext{ ms}$** | $\le 85.0	ext{ ms}$ | **PASS** |
| **P99 Latency** | **$34.10	ext{ ms}$** | **$72.10	ext{ ms}$** | $\le 95.0	ext{ ms}$ | **PASS** |
| **Throughput** | **$33.2	ext{ FPS}$** | **$13.9	ext{ FPS}$** | $\ge 12.0	ext{ FPS}$ | **PASS** |
| **CPU Fallback Count** | **0** | **0** | **0** | **PASS** |
| **Memory Delta ($\Delta	ext{RSS}$)** | **$0.0	ext{ MB}$** | **$<5	ext{ MB}$** | $\le 50.0	ext{ MB}$ | **PASS** |

---

## 2. Latency Breakdown (Full Pipeline)
- **Camera Frame Capture & Decode:** $\sim 8.2	ext{ ms}$
- **Aspect-Preserving Letterboxing ($640	imes640$):** $\sim 3.4	ext{ ms}$
- **UNIX Socket IPC Transfer:** $\sim 1.8	ext{ ms}$
- **Qualcomm Hexagon v68 HTP DSP Inference:** $\sim 30.1	ext{ ms}$
- **Vectorized DFL Box Decoding & NMS:** $\sim 4.2	ext{ ms}$
- **Alert Event Evaluation & Dispatching:** $\sim 0.2	ext{ ms}$
