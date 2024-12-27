import logging
import subprocess

from src.api import app

logging.info(app)


def start_prefect_server():
    print("Starting Prefect server...")
    print("Check out the dashboard at http://127.0.0.1:4200/flows")
    process = subprocess.Popen(["prefect", "server", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def run():
    import uvicorn
    from dotenv import load_dotenv
    from src.__infra__.env import get_env

    print("Starting API server...")
    prefect_process = start_prefect_server()

    try:
        load_dotenv()
        server_host = get_env("SERVER_HOST")
        server_port = int(get_env("SERVER_PORT"))
        debug_mode = get_env("DEBUG_MODE")
        reload = True if debug_mode.lower() == "true" else False

        uvicorn.run(
            "main:app",
            host=server_host,
            port=server_port,
            reload=reload,
            reload_excludes=["logs/*", "temp/*"]
        )
    finally:
        print("Stopping Prefect server...")
        prefect_process.terminate()
        prefect_process.wait()


if __name__ == "__main__":
    run()
