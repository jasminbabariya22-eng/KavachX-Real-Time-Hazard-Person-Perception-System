# KavachX — Live Camera Perception & Client Demonstration Guide

This guide explains how **KavachX** operates with real physical cameras, details the live demonstration video recorded directly on the **Qualcomm Hexagon v68 HTP DSP**, and provides step-by-step instructions for presenting a live demonstration to clients and evaluators.

---

## 1. Live Demonstration Video Package

A complete, high-definition recorded demonstration video captured directly from the **Qualcomm QCS6490 hardware** is available in this repository:

### 🎥 **Demo Video File:**
- **Local Path:** [`docs/demo/kavachx_live_hardware_demo.mp4`](kavachx_live_hardware_demo.mp4)
- **Target EdgeBox Path:** `/home/work_user2/kawachx_task/demo_output.mp4`
- **Resolution:** $1280 \times 720$ (HD 720p) @ $20\text{ FPS}$
- **Recorded On:** Qualcomm Hexagon v68 HTP DSP via FastRPC (`/dev/fastrpc-cdsp`)

### 📸 **Live Hardware Execution Preview:**
![Live Camera Perception HUD](preview_frame_25.png)

---

## 2. What the Client Sees in the Demo Video

Every video frame contains real-time perception annotations and a transparent Heads-Up Display (HUD) generated live by the edge appliance:

1. **Top Telemetry HUD:**
   - `KAVACHX EDGE SAFETY PERCEPTION | QUALCOMM HEXAGON v68 HTP (100% NPU)`
   - Dynamic per-frame DSP latency badge (e.g., `NPU: 30.5 ms`)
   - Instantaneous throughput counter (e.g., `13.6 FPS`)
2. **Bounding Box Overlays:**
   - **FIRE:** Bounded with corner accents + Confidence badge.
   - **SMOKE:** Bounded with corner accents + Confidence badge.
   - **PERSON:** Bounded with corner accents + Confidence badge.
3. **Bottom Emergency Alert Banner:**
   - Automatically flashes an alarm whenever a hazard is classified:
     `[CRITICAL: HAZARD_DETECTED - FIRE DETECTED]`
     `[WARNING: HAZARD_DETECTED - SMOKE DETECTED]`
   - Features a **3.0-second debounce cooldown** to prevent duplicate alarm flood.

---

## 3. How KavachX Works with Real Live Cameras

KavachX supports three plug-and-play camera ingestion modes without requiring any changes to the neural network or C++ worker daemon:

```mermaid
flowchart TD
    subgraph SENSORS["1. Live Optical Capture Options"]
        CAM_USB["Option A: Physical USB / CSI Camera\n(/dev/video0, /dev/video1)"]
        CAM_RTSP["Option B: Network RTSP Security Camera\n(rtsp://admin:pass@192.168.1.100:554/h264)"]
        CAM_FILE["Option C: Industrial File Stream\n(data/test_images/live_test_stream.mp4)"]
    end

    subgraph ADAPTERS["2. Abstracted Capture Engine (src/kavachx/capture)"]
        CAM_USB --> V4L2_ADAPTER["V4L2Source Adapter\n- Linux Video4Linux2 API\n- Auto-probes resolution & FPS"]
        CAM_RTSP --> RTSP_ADAPTER["RTSPSource Adapter\n- Decodes H.264/H.265 RTSP streams\n- Auto-reconnect with exponential backoff"]
        CAM_FILE --> FILE_ADAPTER["VideoSource Adapter\n- Deterministic test driver\n- Loops seamlessly for continuous testing"]
    end

    subgraph CORE_PIPELINE["3. Real-Time Processing Pipeline"]
        V4L2_ADAPTER & RTSP_ADAPTER & FILE_ADAPTER --> QUEUE["Bounded Frame Queue (maxsize=2)\n[Latest-Frame-Wins Policy]"]
        QUEUE --> FASTRPC["Qualcomm FastRPC Transport (/dev/fastrpc-cdsp)"]
        FASTRPC --> DSP["Qualcomm Hexagon v68 HTP DSP\n[100% Neural Execution | 0 CPU Fallback]"]
        DSP --> ALERTS["🚨 Real-Time Security Alert Sinks"]
    end
```

---

## 4. How to Connect a Real Camera in Production

To switch the input source from a video feed to a live camera, simply update [`config/production.json`](../../config/production.json):

### **Mode A: Physical USB or CSI Camera (e.g. Radxa Camera / Logitech Webcam)**
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

### **Mode B: Industrial RTSP IP Camera (e.g. Hikvision, Dahua, Axis)**
```json
{
  "stream": {
    "source_type": "rtsp",
    "source": "rtsp://admin:password@192.168.1.120:554/Streaming/Channels/101",
    "width": 1920,
    "height": 1080,
    "queue_maxsize": 2
  }
}
```

### **Mode C: File/Synthetic Stream (Default Benchmark Mode)**
```json
{
  "stream": {
    "source_type": "video",
    "source": "/home/work_user2/kawachx_task/test_images/live_test_stream.mp4",
    "loop": true,
    "queue_maxsize": 2
  }
}
```

---

## 5. Step-by-Step Commands to Run Live Demo for Clients

### Option 1: Live Interactive Terminal Console
To show the client live frame-by-frame inference running directly on the Qualcomm Hexagon DSP:
```powershell
# From Windows VS Code Terminal:
python tools/target_runner.py "cd /home/work_user2/kawachx_task && python3 tools/live_camera_viewer.py 30"
```
**What the client sees:** Real-time console logs showing milliseconds latency (`~30.5 ms`), detected classes (`SMOKE`, `FIRE`, `PERSON`), pixel coordinates, and live alert tags `🚨 [WARNING: HAZARD_DETECTED - SMOKE]`.

---

### Option 2: Record a Fresh Demo Video Live
To record a new MP4 video on the fly from the current camera feed:
```powershell
python tools/target_runner.py "cd /home/work_user2/kawachx_task && python3 tools/generate_annotated_demo_video.py live_demo.mp4 100"
```

---

### Option 3: Play the Pre-Recorded Hardware Demo Video
Double-click and open the local video file on your workstation:
- **`docs/demo/kavachx_live_hardware_demo.mp4`**

This video runs at full HD resolution with complete HUD telemetry and bounding box tracking, providing proof that the model and hardware acceleration are operating as specified.
