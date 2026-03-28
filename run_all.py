import subprocess
import sys
import os
import subprocess
import sys
import os
import signal
import time

from util.logger import setup_logger

processes = []

logger = setup_logger("run_all")


def start_service(name, path):
    logger.info(f"Starting {name} at {path}...")
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=path
    )
    processes.append(process)


def stop_all():
    logger.info("Stopping all services...")
    for p in processes:
        try:
            p.terminate()
        except Exception:
            logger.exception("Failed to terminate a process")


def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Start services
        start_service("Detector Service", os.path.join(base_dir, "detector_service"))
        start_service("Grouping Service", os.path.join(base_dir, "grouping_service"))
        start_service("Gateway Service", os.path.join(base_dir, "gateway"))

        logger.info("All services started")
        logger.info("Gateway:   http://127.0.0.1:5000")
        logger.info("Detector:  http://127.0.0.1:8001")
        logger.info("Grouping:  http://127.0.0.1:8002")

        logger.info("Press CTRL+C to stop all services...")

        # Keep alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_all()


if __name__ == "__main__":
    main()