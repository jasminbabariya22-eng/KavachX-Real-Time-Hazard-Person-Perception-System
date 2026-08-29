#!/usr/bin/env python3
"""
generate_annotated_demo_video.py
--------------------------------
Ingests live camera / stream frames, executes inference on Qualcomm Hexagon v68 HTP DSP,
renders bounding boxes, confidence badges, telemetry overlay, and hazard alert banners,
and records the result to a high-quality MP4 demonstration video.
"""

import os
import sys
import time
import cv2
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from kavachx.config.loader import load_config
from kavachx.capture.camera import create_capture_source
from kavachx.inference.engine import InferenceEngine
from kavachx.pipeline.events import AlertEventManager

COLOR_MAP = {
    "fire": (0, 0, 255),       # Vibrant Red
    "smoke": (0, 140, 255),    # High-visibility Amber / Orange
    "person": (255, 215, 0),   # Neon Cyan-Yellow
}

def draw_hud(frame, frame_idx, dsp_latency_ms, fps, alert_text=None, alert_severity="WARNING"):
    h, w = frame.shape[:2]

    # 1. Top Header Glassmorphism Bar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 54), (18, 22, 28), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    cv2.line(frame, (0, 54), (w, 54), (0, 200, 255), 2)

    title = "KAVACHX EDGE SAFETY PERCEPTION | QUALCOMM HEXAGON v68 HTP (100% NPU)"
    cv2.putText(frame, title, (16, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (255, 255, 255), 2, cv2.LINE_AA)

    # Telemetry Badge on Right
    telemetry = f"FRAME #{frame_idx:03d} | NPU: {dsp_latency_ms:4.1f} ms | {fps:4.1f} FPS"
    tw = cv2.getTextSize(telemetry, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)[0][0]
    cv2.putText(frame, telemetry, (w - tw - 16, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 180), 2, cv2.LINE_AA)

    # 2. Bottom Alert Banner if Hazard Active
    if alert_text:
        alert_overlay = frame.copy()
        cv2.rectangle(alert_overlay, (0, h - 50), (w, h), (0, 0, 160) if alert_severity == "CRITICAL" else (0, 100, 200), -1)
        cv2.addWeighted(alert_overlay, 0.85, frame, 0.15, 0, frame)
        cv2.line(frame, (0, h - 50), (w, h - 50), (0, 0, 255) if alert_severity == "CRITICAL" else (0, 165, 255), 2)
        cv2.putText(frame, alert_text, (20, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (255, 255, 255), 2, cv2.LINE_AA)

def draw_detection(frame, det):
    x1, y1, x2, y2 = [int(v) for v in det.bbox]
    cls = det.class_name.lower()
    color = COLOR_MAP.get(cls, (0, 255, 0))
    conf = det.confidence * 100.0

    # Ensure coords within frame
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w - 1, x2), min(h - 1, y2)

    # Bounding Box with Corner Accents
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    corner_len = min(20, (x2 - x1) // 4, (y2 - y1) // 4)
    if corner_len > 4:
        # Top-left corner
        cv2.line(frame, (x1, y1), (x1 + corner_len, y1), color, 4)
        cv2.line(frame, (x1, y1), (x1, y1 + corner_len), color, 4)
        # Bottom-right corner
        cv2.line(frame, (x2, y2), (x2 - corner_len, y2), color, 4)
        cv2.line(frame, (x2, y2), (x2, y2 - corner_len), color, 4)

    # Label Badge with Shadow
    label = f"{det.class_name.upper()} {conf:.1f}%"
    (lw, lh), base = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    by1 = max(0, y1 - lh - 8)
    by2 = max(lh + 8, y1)
    bx2 = min(w - 1, x1 + lw + 12)

    # Badge background
    cv2.rectangle(frame, (x1, by1), (bx2, by2), color, -1)
    text_color = (0, 0, 0) if cls in ["person", "smoke"] else (255, 255, 255)
    cv2.putText(frame, label, (x1 + 6, by2 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, text_color, 2, cv2.LINE_AA)

def record_demo(output_video_path="demo_output.mp4", max_frames=90):
    cfg = load_config()
    source_cfg = cfg.get("stream", {})

    # Auto-resolve video or camera source
    if source_cfg.get("source_type") == "video":
        possible_paths = [
            "/home/work_user2/kawachx_task/test_images/live_test_stream.mp4",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/test_images/live_test_stream.mp4")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_images/live_test_stream.mp4"))
        ]
        for p in possible_paths:
            if os.path.exists(p):
                source_cfg["source"] = p
                break

    src = create_capture_source(source_cfg)
    if not src.open():
        print(f"[ERROR] Could not open camera source: {source_cfg.get('source')}")
        return False

    engine = InferenceEngine()
    if not engine.connect():
        print("[ERROR] Could not connect to NPU worker daemon.")
        src.close()
        return False

    event_mgr = AlertEventManager(cfg.get("alerting", {}))

    print("==================================================================")
    print("  RECORDING LIVE PERCEPTION DEMO VIDEO")
    print(f"  Camera Source: {source_cfg.get('source_type', 'camera').upper()} ({source_cfg.get('source')})")
    print(f"  Target Frames: {max_frames} frames (~3-5 seconds continuous stream)")
    print(f"  Output Video:  {output_video_path}")
    print("==================================================================")

    writer = None
    frame_count = 0
    start_time = time.time()
    current_alert = None
    current_severity = "WARNING"
    alert_expiry = 0

    try:
        while frame_count < max_frames:
            t0 = time.time()
            ok, frame, ts, f_id = src.read()
            if not ok or frame is None:
                print("[INFO] End of stream or capture timeout.")
                break

            frame_count += 1
            h, w = frame.shape[:2]

            # Lazy init VideoWriter with matching dimensions
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(output_video_path, fourcc, 20.0, (w, h))

            # Run NPU inference on Qualcomm Hexagon DSP
            out = engine.infer(frame, req_id=frame_count)

            # Process event pipeline
            dispatched = event_mgr.process(out.detections)
            now = time.time()
            if dispatched:
                current_alert = f"[{dispatched[0]['severity']}: {dispatched[0]['event_type']} - {dispatched[0]['class_name'].upper()} DETECTED]"
                current_severity = dispatched[0]['severity']
                alert_expiry = now + 2.5
            elif now > alert_expiry:
                current_alert = None

            # Render detections onto frame
            for det in out.detections:
                draw_detection(frame, det)

            # Calculate instantaneous FPS
            dt = time.time() - t0
            fps = 1.0 / max(0.001, dt)

            # Draw HUD
            draw_hud(frame, frame_count, out.infer_time_ms, fps, current_alert, current_severity)

            # Write frame to video
            writer.write(frame)

            print(f"  [FRAME {frame_count:02d}/{max_frames}] Latency: {out.infer_time_ms:5.2f} ms | Detections: {len(out.detections)} | FPS: {fps:4.1f}")

    finally:
        if writer is not None:
            writer.release()
        src.close()
        engine.close()

    total_time = time.time() - start_time
    avg_fps = frame_count / max(0.001, total_time)
    print("==================================================================")
    print(f"  [SUCCESS] Demo video recorded: {output_video_path}")
    print(f"  Processed {frame_count} frames in {total_time:.2f}s (Avg {avg_fps:.1f} FPS)")
    print("==================================================================")
    return True

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "demo_output.mp4"
    num_frames = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    record_demo(out_file, num_frames)
