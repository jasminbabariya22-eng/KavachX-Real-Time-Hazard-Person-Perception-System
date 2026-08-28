# Camera Ingestion & Integration Guide

## 1. Supported Ingestion Modes

KavachX supports three continuous input modes configured via `config/production.json`:

### 1.1 Local V4L2 USB / CSI Camera (`/dev/video0`)
Connect a USB or CSI camera to the EdgeBox.
```json
{
  "stream": {
    "source_type": "camera",
    "source": "/dev/video0",
    "width": 1280,
    "height": 720,
    "target_fps": 30.0,
    "queue_maxsize": 2
  }
}
```

### 1.2 Network RTSP Security IP Camera
Stream from an IP security camera over RTSP with automatic backoff and reconnection:
```json
{
  "stream": {
    "source_type": "rtsp",
    "source": "rtsp://admin:password@192.168.1.100:554/live",
    "reconnect_backoff_sec": 1.0,
    "max_reconnect_attempts": 5,
    "target_fps": 30.0,
    "queue_maxsize": 2
  }
}
```

### 1.3 Continuous Video File Feed
Stream from a local video file for automated validation:
```json
{
  "stream": {
    "source_type": "video",
    "source": "test_data/videos/live_test_stream.mp4",
    "capture_fps": 30.0,
    "loop": true,
    "queue_maxsize": 2
  }
}
```
