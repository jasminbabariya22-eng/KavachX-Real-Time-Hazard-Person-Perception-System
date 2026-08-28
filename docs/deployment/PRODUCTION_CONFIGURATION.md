# Production Configuration Specification

## 1. Configuration File Layout (`config/production.json`)

```json
{
  "system": {
    "app_name": "KavachX",
    "version": "1.0.0",
    "log_level": "INFO",
    "health_file": "/tmp/kawach_health.json"
  },
  "inference": {
    "model_path": "/home/work_user2/kawachx_task/models/production/3class_calibrated_final.bin",
    "ipc_socket_path": "/tmp/kawach_worker.sock",
    "input_width": 640,
    "input_height": 640,
    "confidence_threshold": 0.25,
    "nms_iou_threshold": 0.45,
    "classes": ["fire", "smoke", "person"]
  },
  "stream": {
    "source_type": "video",
    "source": "/home/work_user2/kawachx_task/test_images/live_test_stream.mp4",
    "width": 1280,
    "height": 720,
    "capture_fps": 30.0,
    "queue_maxsize": 2,
    "loop": true
  },
  "alerting": {
    "cooldown_seconds": 3.0,
    "fire_severity": "CRITICAL",
    "smoke_severity": "WARNING",
    "person_severity": "WARNING"
  }
}
```
