# Incident Recovery Procedures

## 1. Automated & Manual Recovery Steps
1. **Worker Crash:** `tools/service_manager.py` detects dead PID, unlinks stale `/tmp/kawach_worker.sock`, and restarts worker daemon.
2. **Camera Feed Drop:** `RTSPSource` applies exponential backoff ($1\text{s}, 2\text{s}, 4\text{s}$) and reconnects without dropping the DSP context.
3. **Manual Hard Reset:**
   ```bash
   python3 tools/service_manager.py restart
   cat /tmp/kawach_health.json
   ```
