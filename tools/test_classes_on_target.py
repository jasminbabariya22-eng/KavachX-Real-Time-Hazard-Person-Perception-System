import cv2
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from kavachx.inference.engine import InferenceEngine

def test_inference():
    eng = InferenceEngine()
    if not eng.connect():
        print("Could not connect")
        return

    test_imgs = ["fire.jpg", "fire_2.jpg", "person.jpg"]
    base_dir = "/home/work_user2/kawachx_task/test_images"
    
    for name in test_imgs:
        p = os.path.join(base_dir, name)
        if not os.path.exists(p):
            print(f"File not found: {p}")
            continue
        img = cv2.imread(p)
        out = eng.infer(img)
        print(f"\n=== Image: {name} ===")
        print(f"Raw detection count: {len(out.detections)}")
        for d in out.detections[:5]:
            print(f"  Class: {d.class_name} (ID: {d.class_id}) | Conf: {d.confidence*100:.1f}% | Box: {d.bbox}")
    eng.close()

if __name__ == "__main__":
    test_inference()
