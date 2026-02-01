import subprocess


def main():
    """Main entry point that launches both API and frontend services."""
    # Create logs directory
    import os

    os.makedirs("logs", exist_ok=True)

    # Launch new restructured API service
    api_proc = subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload", "--port", "8000"]
    )

    # # Launch fastHtml Fonrtend Service
    # frontend_proc = subprocess.Popen(
    #     ["uvicorn", "frontend_fastHtml.main:app", "--reload", "--port", "8080"]
    # )

    # Launch React Fonrtend Service
    frontend_proc = subprocess.Popen(["npm", "--prefix", "frontend_react", "start"])

    try:
        print("🚀 Starting services...")
        print("📡 API service: http://localhost:8000")
        print("🌐 Frontend service: http://localhost:8080")
        print("📚 API Docs: http://localhost:8000/docs")
        print("📝 Logs directory: ./logs/")
        print("Press Ctrl+C to stop all services")

        api_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        api_proc.terminate()
        frontend_proc.terminate()
        print("✅ All services stopped")


if __name__ == "__main__":
    main()
