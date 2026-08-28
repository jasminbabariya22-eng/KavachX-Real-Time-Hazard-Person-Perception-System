# Reliability & Failure Recovery Specification

## 1. Resilience Features
1. **Zero Memory Leak Guarantee:** Sustained tests over 500+ frames demonstrate flat RSS memory consumption ($\Delta	ext{RSS} < 5	ext{ MB}$).
2. **Process Isolation:** The native C++ worker runs as an independent daemon. Crashing clients or dropped camera streams cannot corrupt the DSP session.
3. **Supervisor Self-Healing:** `tools/service_manager.py` verifies process liveness and automatically restores crashed workers.
4. **Clean Socket Cleanup:** SIGINT/SIGTERM handlers unlink `/tmp/kawach_worker.sock` and clean up FastRPC context handles cleanly.
