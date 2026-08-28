# Streaming & Throughput Testing

## 1. Streaming Test Suite (`tests/streaming/test_live_stream.py`)
Streams 40+ continuous live frames through the end-to-end pipeline:
- **Throughput:** $13.9\text{ FPS}$ sustained.
- **Mean Pipeline Latency:** $61.91\text{ ms}$.
- **Memory Growth ($\Delta\text{RSS}$):** Flat ($<5\text{ MB}$).
