"""DFL Box Decoder & Postprocessor with Non-Maximum Suppression (NMS)."""
import cv2
import numpy as np
from typing import List, Optional
from .model import Detection

# Exact Ultralytics Class Mapping for the 3-class model
DEFAULT_CLASSES = ["person", "fire", "smoke"]

def decode_detections(
    tensor_7x8400: np.ndarray,
    r: float,
    dw: float,
    dh: float,
    conf_thresh: float = 0.25,
    iou_thresh: float = 0.45,
    class_names: Optional[List[str]] = None,
    orig_shape: Optional[tuple] = None
) -> List[Detection]:
    """
    Decodes the [7, 8400] output tensor from the Qualcomm NPU / DFL decoder,
    applies unletterboxing, and performs Non-Maximum Suppression (NMS).
    
    Layout of tensor_7x8400:
      Row 0: cx
      Row 1: cy
      Row 2: w
      Row 3: h
      Row 4: score_person (Class 0)
      Row 5: score_fire   (Class 1)
      Row 6: score_smoke  (Class 2)
    """
    if class_names is None:
        class_names = DEFAULT_CLASSES

    # Transpose to [8400, 7]
    preds = tensor_7x8400.T
    boxes = preds[:, :4]    # [8400, 4] -> cx, cy, w, h
    scores = preds[:, 4:7]  # [8400, 3] -> person, fire, smoke

    class_ids = np.argmax(scores, axis=1)
    confidences = np.max(scores, axis=1)

    # 1. Filter by confidence threshold
    mask = confidences >= conf_thresh
    boxes = boxes[mask]
    scores_filtered = confidences[mask]
    class_ids_filtered = class_ids[mask]

    if len(boxes) == 0:
        return []

    # 2. Unletterbox: map 640x640 letterboxed coordinates back to original frame
    x1 = (boxes[:, 0] - boxes[:, 2] / 2.0 - dw) / r
    y1 = (boxes[:, 1] - boxes[:, 3] / 2.0 - dh) / r
    x2 = (boxes[:, 0] + boxes[:, 2] / 2.0 - dw) / r
    y2 = (boxes[:, 1] + boxes[:, 3] / 2.0 - dh) / r

    if orig_shape is not None:
        x1 = np.clip(x1, 0, orig_shape[1])
        y1 = np.clip(y1, 0, orig_shape[0])
        x2 = np.clip(x2, 0, orig_shape[1])
        y2 = np.clip(y2, 0, orig_shape[0])

    # 3. Prepare OpenCV format boxes [x, y, w, h] for NMS
    w_box = x2 - x1
    h_box = y2 - y1
    cv_boxes = [[int(x1[i]), int(y1[i]), int(w_box[i]), int(h_box[i])] for i in range(len(x1))]

    # 4. Multi-class Non-Maximum Suppression (NMS)
    indices = cv2.dnn.NMSBoxes(cv_boxes, scores_filtered.tolist(), conf_thresh, iou_thresh)

    detections = []
    if len(indices) > 0:
        for idx in indices.flatten():
            cid = int(class_ids_filtered[idx])
            cname = class_names[cid] if cid < len(class_names) else f"class_{cid}"
            conf = float(scores_filtered[idx])
            bx1 = float(x1[idx])
            by1 = float(y1[idx])
            bx2 = float(x2[idx])
            by2 = float(y2[idx])

            detections.append(Detection(
                class_id=cid,
                class_name=cname,
                confidence=round(conf, 3),
                bbox=[round(bx1, 1), round(by1, 1), round(bx2, 1), round(by2, 1)]
            ))

    return detections
