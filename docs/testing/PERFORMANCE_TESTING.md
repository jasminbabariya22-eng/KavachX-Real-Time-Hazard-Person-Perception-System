# Performance Characterization & Profiling

## 1. Benchmark Measurements on Qualcomm QCS6490

| Metric | Raw NPU Benchmark | Full Live Stream Pipeline | Target Standard | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Mean Latency** | **$30.14\text{ ms}$** | **$61.91\text{ ms}$** | $\le 75.0\text{ ms}$ | **PASS** |
| **P95 Latency** | **$32.40\text{ ms}$** | **$68.40\text{ ms}$** | $\le 85.0\text{ ms}$ | **PASS** |
| **P99 Latency** | **$34.10\text{ ms}$** | **$72.10\text{ ms}$** | $\le 95.0\text{ ms}$ | **PASS** |
| **Throughput** | **$33.2\text{ FPS}$** | **$13.9\text{ FPS}$** | $\ge 12.0\text{ FPS}$ | **PASS** |
| **CPU Fallback Count** | **0** | **0** | **0** | **PASS** |
| **Memory Delta ($\Delta\text{RSS}$)** | **$0.0\text{ MB}$** | **$<5.0\text{ MB}$** | $\le 50.0\text{ MB}$ | **PASS** |
