import os
import sys
import requests
from config import DETECTOR_URL, GROUPING_URL, REQUEST_TIMEOUT

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.logger import setup_logger

logger = setup_logger("gateway.client")


def call_detector(file):
    logger.info(f"Calling detector at {DETECTOR_URL}")
    try:
        response = requests.post(
            DETECTOR_URL,
            files={"image": (file.filename, file.stream, file.mimetype)},
            timeout=REQUEST_TIMEOUT
        )

        logger.info(f"Detector response: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Detector service failed: {response.status_code} {response.text}")
            raise Exception("Detector service failed")

        return response.json()

    except Exception:
        logger.exception("Error calling detector service")
        raise


def call_grouping(detector_output):
    logger.info(f"Calling grouping at {GROUPING_URL}")
    try:
        response = requests.post(
            GROUPING_URL,
            json=detector_output,
            timeout=REQUEST_TIMEOUT
        )

        logger.info(f"Grouping response: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Grouping service failed: {response.status_code} {response.text}")
            raise Exception("Grouping service failed")

        return response.json()

    except Exception:
        logger.exception("Error calling grouping service")
        raise