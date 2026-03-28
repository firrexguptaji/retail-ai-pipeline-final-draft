import os

MODEL_PATH = os.getenv("MODEL_PATH", "model\\yolov8n.pt")

SLICE_SIZE = int(os.getenv("SLICE_SIZE", 512))
OVERLAP = float(os.getenv("OVERLAP", 0.4))

IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", 0.4))

MIN_AREA_RATIO = float(os.getenv("MIN_AREA_RATIO", 0.0005))
MAX_AREA_RATIO = float(os.getenv("MAX_AREA_RATIO", 0.03))