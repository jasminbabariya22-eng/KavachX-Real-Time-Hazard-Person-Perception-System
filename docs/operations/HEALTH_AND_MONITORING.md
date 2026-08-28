# Health & Monitoring Specification

## 1. Machine-Readable Health Endpoint (`/tmp/kawach_health.json`)

The supervisor daemon maintains a real-time health file:

```json
{
  "service": "kawach_worker",
  "state": "READY",
  "timestamp": "2026-08-27T15:58:45Z",
  "details": {
    "pid": 255925,
    "model": "/home/work_user2/kawachx_task/models/production/3class_calibrated_final.bin",
    "socket": "/tmp/kawach_worker.sock"
  }
}
```

---

## 2. Operational Health States
- **`READY`:** Daemon is running, FastRPC session active, socket listening for requests.
- **`STARTING`:** Daemon initializing QNN backend and deserializing context binary.
- **`FAILED`:** Process exited prematurely or FastRPC device node inaccessible.
- **`STOPPED`:** Daemon stopped cleanly by operator.
