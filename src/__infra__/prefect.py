import signal
import subprocess


def run_local_prefect() -> str:
    print("Starting Prefect server...")
    server_info = "Prefect: http://localhost:4200"
    print(server_info)
    with open("third_party.txt", "a") as file:
        file.write(f"{server_info}\n")

    process = subprocess.Popen(["prefect", "server", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def signal_handler(sig, frame):
        print("Stopping the Prefect server...")
        process.terminate()
        process.wait()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    return server_info
