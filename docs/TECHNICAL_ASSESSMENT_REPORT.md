# KavachX — Technical Assessment & Deployment Report

## 1. Executive Summary
KavachX is an edge-deployed computer vision system for industrial safety monitoring (Fire, Smoke, and Person detection) running on-device on the **Qualcomm QCS6490 SoC** with **100% neural network execution on the Qualcomm Hexagon v68 HTP DSP**.

---

## 2. Key Verified Results
- **Model Checksum:** `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc` ($26.8\text{ MB}$, INT8).
- **FastRPC Transport:** Active via `/dev/fastrpc-cdsp` (GID `993` render group).
- **Raw NPU Inference Latency:** **$30.14\text{ ms}$** ($\sim 33.2\text{ FPS}$).
- **End-to-End Live Stream Pipeline:** **$61.91\text{ ms}$** ($\sim 13.9\text{ FPS}$).
- **CPU Fallback:** **0 Layers**.
- **Numerical Parity vs. FP32:** $100\%$ Top-1 class agreement, $0.912$ Mean Box IoU overlap.
