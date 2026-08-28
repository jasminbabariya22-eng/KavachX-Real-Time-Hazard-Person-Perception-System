# Production Operations Runbook

## 1. Quick Service Commands

| Operation | Command | Expected Output |
| :--- | :--- | :--- |
| **Start Service** | `python3 tools/service_manager.py start` | `kawach_worker successfully started (PID ...) — READY` |
| **Stop Service** | `python3 tools/service_manager.py stop` | `kawach_worker stopped successfully` |
| **Restart Service** | `python3 tools/service_manager.py restart` | `kawach_worker successfully started (PID ...) — READY` |
| **Service Status** | `python3 tools/service_manager.py status` | `Status: RUNNING, State: READY, Socket: ACTIVE` |
| **Health Check** | `cat /tmp/kawach_health.json` | `{"service": "kawach_worker", "state": "READY", ...}` |

---

## 2. Troubleshooting Procedures

### 2.1 FastRPC Permission Denied
- **Symptom:** Worker fails with `Failed to open /dev/fastrpc-cdsp`.
- **Remedy:** Ensure user is in `render` group:
  ```bash
  sudo usermod -a -G render $USER
  ```

### 2.2 Worker Socket Missing
- **Symptom:** Client reports `FileNotFoundError: /tmp/kawach_worker.sock`.
- **Remedy:** Inspect worker logs:
  ```bash
  cat /tmp/kawach_worker.log
  ```
  Restart service:
  ```bash
  python3 tools/service_manager.py restart
  ```
