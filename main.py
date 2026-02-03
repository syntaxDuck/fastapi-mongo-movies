import subprocess
import argparse
import os


def main():
    """Main entry point that launches both API and frontend services."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--backend", action="store_true", help="Start backend service"
    )
    parser.add_argument(
        "-f", "--frontend", action="store_true", help="Start frontend service"
    )
    args = parser.parse_args()

    os.makedirs("logs", exist_ok=True)

    if not args.backend and not args.frontend:
        args.backend = args.frontend = True

    api_proc = None
    if args.backend:
        api_proc = subprocess.Popen(
            ["uvicorn", "app.main:app", "--reload", "--port", "8000"]
        )

    frontend_proc = None
    if args.frontend:
        frontend_proc = subprocess.Popen(["npm", "--prefix", "frontend_react", "start"])

    try:
        print("Starting services...")
        print("API service: http://localhost:8000")
        print("Frontend service: http://localhost:8080")
        print("API Docs: http://localhost:8000/docs")
        print("Logs directory: ./logs/")
        print("Press Ctrl+C to stop all services")

        if api_proc:
            api_proc.wait()

        if frontend_proc:
            frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        if api_proc:
            api_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        print("All services stopped")


if __name__ == "__main__":
    main()
