import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import setup_logger

from flask import Flask, request, jsonify
import numpy as np
import cv2
import base64

from detector import detect_products

app = Flask(__name__)

logger = setup_logger("detector_service")
model_loaded = False

def load_model_once():
    global model_loaded
    # your existing model load
    model_loaded = True
    
    
@app.route("/health", methods=["GET"])
def health():
    return {"service": "detector", "status": "ok"}, 200

@app.route("/ready")
def ready():
    if not model_loaded:
        return {"status": "not ready", "reason": "model not loaded"}, 503

    return {"service": "detector", "status": "ready"}, 200

def encode_image(image):
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode("utf-8")


@app.route("/detect", methods=["POST"])
def detect():
    try:

        logger.info("/detect request received")

        if "image" not in request.files:
            logger.warning("No image provided in request")
            return jsonify({"error": "No image provided"}), 400

        file = request.files["image"]

        # Read image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Detection
        boxes, crops = detect_products(image)
        logger.info(f"Detection completed: {len(boxes)} boxes, {len(crops)} crops")

        # Encode crops
        encoded_crops = [encode_image(crop) for crop in crops]

        # Encode full image
        encoded_image = encode_image(image)

        return jsonify({
            "boxes": boxes,
            "crops": encoded_crops,
            "image": encoded_image
        })

    except Exception as e:
        logger.exception("Error in /detect endpoint")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Starting Detector Service on port 8001")
    app.run(port=8001, debug=True)