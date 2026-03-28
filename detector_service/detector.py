from ultralytics import YOLO
import cv2
import numpy as np
import time
import torch
from torchvision.ops import nms

from config import (
    MODEL_PATH,
    SLICE_SIZE,
    OVERLAP,
    IOU_THRESHOLD,
    MIN_AREA_RATIO,
    MAX_AREA_RATIO
)

from util.logger import setup_logger

logger = setup_logger("detector")

# Load model
model = YOLO(MODEL_PATH)
logger.info(f"Loaded YOLO model from {MODEL_PATH}")


# -------------------------------
# Sliding Window (Notebook Match)
# -------------------------------
def sliding_window(image):
    h, w, _ = image.shape
    step = int(SLICE_SIZE * (1 - OVERLAP))

    for y in range(0, h, step):
        for x in range(0, w, step):

            y2 = min(y + SLICE_SIZE, h)
            x2 = min(x + SLICE_SIZE, w)

            crop = image[y:y2, x:x2]

            if crop.shape[0] < 50 or crop.shape[1] < 50:
                continue

            yield x, y, crop


# -------------------------------
# MAIN DETECTION
# -------------------------------
def detect_products(image):
    start = time.time()

    h_img, w_img, _ = image.shape
    img_area = h_img * w_img

    all_boxes = []
    windows = 0

    # 1️⃣ Sliding window + YOLO
    for x_offset, y_offset, window in sliding_window(image):
        windows += 1

        results = model(window, conf=0.03)[0]

        if len(results.boxes) == 0:
            continue

        for box in results.boxes.xyxy.cpu().numpy():
            x1, y1, x2, y2 = map(int, box)

            x1 += x_offset
            x2 += x_offset
            y1 += y_offset
            y2 += y_offset

            all_boxes.append([x1, y1, x2, y2])

    # 2️⃣ Area filtering (relative)
    filtered_boxes = []
    for x1, y1, x2, y2 in all_boxes:
        area = (x2 - x1) * (y2 - y1)

        if MIN_AREA_RATIO * img_area < area < MAX_AREA_RATIO * img_area:
            filtered_boxes.append([x1, y1, x2, y2])

    if len(filtered_boxes) == 0:
        return [], []

    # 3️⃣ Torch NMS (prefer smaller boxes)
    boxes_tensor = torch.tensor(filtered_boxes, dtype=torch.float32)

    areas = (boxes_tensor[:, 2] - boxes_tensor[:, 0]) * (boxes_tensor[:, 3] - boxes_tensor[:, 1])
    scores = 1 / (areas + 1e-6)

    keep = nms(boxes_tensor, scores, iou_threshold=IOU_THRESHOLD)
    filtered_boxes = boxes_tensor[keep].int().tolist()

    # 4️⃣ Remove duplicates (notebook logic)
    unique_boxes = []

    for box in filtered_boxes:
        x1, y1, x2, y2 = box

        keep = True
        for bx1, by1, bx2, by2 in unique_boxes:
            if abs(x1 - bx1) < 10 and abs(y1 - by1) < 10:
                keep = False
                break

        if keep:
            unique_boxes.append(box)

    filtered_boxes = unique_boxes

    # 5️⃣ Remove wide boxes (aspect ratio filter)
    clean_boxes = []

    for x1, y1, x2, y2 in filtered_boxes:
        width = x2 - x1
        height = y2 - y1

        if height == 0:
            continue

        aspect_ratio = width / height

        if aspect_ratio < 3:
            clean_boxes.append([x1, y1, x2, y2])

    filtered_boxes = clean_boxes

    # 6️⃣ Crop extraction (padding + resize)
    crops = []
    final_boxes = []

    for (x1, y1, x2, y2) in filtered_boxes:

        # padding
        pad = 5
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(w_img, x2 + pad)
        y2 = min(h_img, y2 + pad)

        crop = image[y1:y2, x1:x2]

        if crop.size == 0:
            continue

        # resize (match notebook)
        crop = cv2.resize(crop, (224, 224))

        crops.append(crop)
        final_boxes.append([x1, y1, x2, y2])

    elapsed = time.time() - start

    logger.info(
        f"detect_products: windows={windows}, raw={len(all_boxes)}, "
        f"after_filter={len(filtered_boxes)}, final={len(final_boxes)}, time={elapsed:.2f}s"
    )

    return final_boxes, crops