import os

DETECTOR_URL = os.getenv(
    "DETECTOR_URL",
    "http://detector:8001/detect"
)

GROUPING_URL = os.getenv(
    "GROUPING_URL",
    "http://grouping:8002/group"
)

DETECTOR_READY_URL = os.getenv(
    "DETECTOR_READY_URL",
    "http://detector:8001/ready"
)

GROUPING_READY_URL = os.getenv(
    "GROUPING_READY_URL",
    "http://grouping:8002/ready"
)

REQUEST_TIMEOUT = 30