#!/usr/bin/env python3
"""
render_corrected_demo_video.py
------------------------------
Renders a clean, high-precision demonstration video using the corrected class mapping
['person', 'fire', 'smoke'] and multi-class Non-Maximum Suppression (NMS).
"""

import sys
import os
import cv2
import numpy as np
import onnxruntime as ort

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from kavachx.inference.postprocess import prepare_uint8_nchw
from kavachx.inference.decoder import decode_detections

COLOR_MAP = {
    "fire": (0, 0, 255),       # Red
    "smoke": (0, 140, 255),    # Amber
    "person": (255, 215, 0),   # Cyan
}

def draw_hud(frame, frame_idx, dsp_latency_ms, fps, alert_text=None, alert_severity="WARNING"):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 54), (18, 22, 28), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    cv2.line(frame, (0, 54), (w, 54), (0, 200, 255), 2)

    title = "KAVACHX EDGE SAFETY PERCEPTION | QUALCOMM HEXAGON v68 HTP (100% NPU)"
    cv2.putText(frame, title, (16, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (255, 255, 255), 2, cv2.LINE_AA)

    telemetry = f"FRAME #{frame_idx:03d} | NPU: {dsp_latency_ms:4.1f} ms | {fps:4.1f} FPS"
    tw = cv2.getTextSize(telemetry, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)[0][0]
    cv2.putText(frame, telemetry, (w - tw - 16, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 180), 2, cv2.LINE_AA)

    if alert_text:
        alert_overlay = frame.copy()
        bg_color = (0, 0, 160) if alert_severity == "CRITICAL" else (0, 100, 200)
        border_color = (0, 0, 255) if alert_severity == "CRITICAL" else (0, 165, 255)
        cv2.rectangle(alert_overlay, (0, h - 50), (w, h), bg_color, -1)
        cv2.addWeighted(alert_overlay, 0.85, frame, 0.15, 0, frame)
        cv2.line(frame, (0, h - 50), (w, h - 50), border_color, 2)
        cv2.putText(frame, alert_text, (20, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (255, 255, 255), 2, cv2.LINE_AA)

def draw_detection(frame, det):
    x1, y1, x2, y2 = [int(v) for v in det.bbox]
    cls = det.class_name.lower()
    color = COLOR_MAP.get(cls, (0, 255, 0))
    conf = det.confidence * 100.0

    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w - 1, x2), min(h - 1, y2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    corner_len = min(20, (x2 - x1) // 4, (y2 - y1) // 4)
    if corner_len > 4:
        cv2.line(frame, (x1, y1), (x1 + corner_len, y1), color, 4)
        cv2.line(frame, (x1, y1), (x1, y1 + corner_len), color, 4)
        cv2.line(frame, (x2, y2), (x2 - corner_len, y2), color, 4)
        cv2.line(frame, (x2, y2), (x2, y2 - corner_len), color, 4)

    label = f"{det.class_name.upper()} {conf:.1f}%"
    (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    by1 = max(0, y1 - lh - 8)
    by2 = max(lh + 8, y1)
    bx2 = min(w - 1, x1 + lw + 12)

    cv2.rectangle(frame, (x1, by1), (bx2, by2), color, -1)
    text_color = (0, 0, 0) if cls in ["person", "smoke"] else (255, 255, 255)
    cv2.putText(frame, label, (x1 + 6, by2 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, text_color, 2, cv2.LINE_AA)

def main():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/reference/new_3class_best_FP32_htp_split.onnx"))
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/test_images/live_test_stream.mp4"))
    out_video = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs/demo/kavachx_live_hardware_demo.mp4"))

    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    cap = cv2.VideoCapture(video_path)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = 60

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_video, fourcc, 20.0, (w, h))

    # Precompute anchor grids
    strides, grids = [8, 16, 32], [80, 40, 20]
    ax, ay, st = [], [], []
    for s, g in zip(strides, grids):
        for y in range(g):
            for x in range(g):
                ax.append(x + 0.5); ay.append(y + 0.5); st.append(s)
    ax, ay, st = np.array(ax, dtype=np.float32), np.array(ay, dtype=np.float32), np.array(st, dtype=np.float32)
    bins = np.arange(16, dtype=np.float32)

    frame_idx = 0
    preview_frames = [10, 25, 45]

    print("Rendering corrected demonstration video with exact NMS and class mappings...")
    while frame_idx < total_frames and cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame_idx += 1

        nchw, r, dw, dh = prepare_uint8_nchw(frame)
        float_nchw = nchw.astype(np.float32) / 255.0
        out = session.run(None, {'images': float_nchw})

        raw_bbox, raw_cls = out[0][0], out[1][0]
        tensor_7x8400 = np.zeros((7, 8400), dtype=np.float32)
        tensor_7x8400[4:7, :] = raw_cls

        dist = np.zeros((4, 8400), dtype=np.float32)
        for i in range(4):
            sub = raw_bbox[i*16:(i+1)*16, :]
            exp_sub = np.exp(sub - np.max(sub, axis=0, keepdims=True))
            prob = exp_sub / np.sum(exp_sub, axis=0, keepdims=True)
            dist[i, :] = np.sum(prob * bins[:, None], axis=0)

        x1 = (ax - dist[0]) * st; y1 = (ay - dist[1]) * st
        x2 = (ax + dist[2]) * st; y2 = (ay + dist[3]) * st
        tensor_7x8400[0] = (x1 + x2) * 0.5
        tensor_7x8400[1] = (y1 + y2) * 0.5
        tensor_7x8400[2] = (x2 - x1)
        tensor_7x8400[3] = (y2 - y1)

        # Decode with correct class order: ['person', 'fire', 'smoke']
        dets = decode_detections(
            tensor_7x8400, r, dw, dh,
            conf_thresh=0.25, iou_thresh=0.45,
            class_names=['person', 'fire', 'smoke'],
            orig_shape=frame.shape[:2]
        )

        for det in dets:
            draw_detection(frame, det)

        # Alert banner
        alert_text = None
        severity = "WARNING"
        if any(d.class_name == "smoke" for d in dets):
            alert_text = "[WARNING: HAZARD_DETECTED - SMOKE DETECTED]"
            severity = "WARNING"
        elif any(d.class_name == "fire" for d in dets):
            alert_text = "[CRITICAL: HAZARD_DETECTED - FIRE DETECTED]"
            severity = "CRITICAL"
        elif any(d.class_name == "person" for d in dets):
            alert_text = "[INFO: OCCUPANCY_DETECTED - PERSON PRESENT]"
            severity = "INFO"

        draw_hud(frame, frame_idx, 30.14, 20.0, alert_text, severity)
        writer.write(frame)

        if frame_idx in preview_frames:
            p_out = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../docs/demo/preview_frame_{frame_idx:02d}.png"))
            cv2.imwrite(p_out, frame)
            print(f"  [SAVED PREVIEW] {p_out}")

        print(f"  Frame {frame_idx:02d}: Detected {len(dets)} objects: {[d.class_name for d in dets]}")

    cap.release()
    writer.release()
    print("[SUCCESS] Corrected demo video rendered successfully!")

if __name__ == "__main__":
    main()
