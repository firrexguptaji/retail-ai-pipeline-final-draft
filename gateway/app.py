import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.logger import setup_logger

from flask import Flask, request, jsonify, render_template, send_from_directory
from client import call_detector, call_grouping

app = Flask(__name__)

logger = setup_logger("gateway")


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/outputs/<filename>')
def get_output(filename):
    return send_from_directory('../outputs', filename)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        logger.info("/predict request received")

        if "image" not in request.files:
            logger.warning("No image provided in /predict request")
            return jsonify({"error": "No image provided"}), 400

        file = request.files["image"]

        # Step 1: Detector
        det_data = call_detector(file)
        logger.info("Received detector response")

        # Step 2: Grouping
        grp_data = call_grouping(det_data)
        logger.info("Received grouping response")

        return jsonify(grp_data)

    except Exception as e:
        logger.exception("Error in /predict endpoint")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Starting Gateway Service on port 5000")
    app.run(port=5000, debug=True)