# Troubleshooting & Diagnostic Guide

## 1. Diagnostic Matrix

| Symptom / Error | Root Cause | Resolution Command |
| :--- | :--- | :--- |
| `Failed to open /dev/fastrpc-cdsp` | User not in `render` group. | `sudo usermod -a -G render $USER` |
| `FileNotFoundError: /tmp/kawach_worker.sock` | Worker daemon not running. | `python3 tools/service_manager.py restart` |
| `Model SHA256 Mismatch` | Corrupted context binary. | Verify SHA256 with `tools/model_inspect.py`. |
| `Camera stream timeout` | Camera disconnected or RTSP stream down. | Check camera connection or test with video stream. |
