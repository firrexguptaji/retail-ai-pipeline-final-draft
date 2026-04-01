import subprocess
import sys

services = [
    ("Detector", "detector_service/app.py"),
    ("Grouping", "grouping_service/app.py"),
    ("Gateway", "gateway/app.py"),
]


def start_service(name, path):
    print(f"[STARTING] {name}...")
    return subprocess.Popen([sys.executable, path])


def main():
    processes = []

    try:
        for name, path in services:
            proc = start_service(name, path)
            processes.append(proc)

        print("\nAll services started (DEV MODE)")
        print("Gateway: http://127.0.0.1:5000\n")

        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Stopping all services...")

        for p in processes:
            p.terminate()

        print("All services stopped.")


if __name__ == "__main__":
    main()