import subprocess


def main():
    api_proc = subprocess.Popen(
        ["uvicorn", "api.main:app", "--reload", "--port", "8000"]
    )
    frontend_proc = subprocess.Popen(
        ["uvicorn", "frontend.main:app", "--reload", "--port", "8080"]
    )
    try:
        api_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        api_proc.terminate()
        frontend_proc.terminate()


if __name__ == "__main__":
    main()
