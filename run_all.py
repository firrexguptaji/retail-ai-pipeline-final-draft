import subprocess
import sys

services = [
    ("Detector", "detector_service.app"),
    ("Grouping", "grouping_service.app"),
    ("Gateway", "gateway.app"),
]


def start_service(name, module):
    print(f"[STARTING] {name}...")
    return subprocess.Popen([sys.executable, "-m", module])


def main():
    processes = []

    try:
        for name, module in services:
            proc = start_service(name, module)
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