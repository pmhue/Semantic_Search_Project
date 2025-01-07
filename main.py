import logging
from textwrap import dedent

from src.app import app

logging.info(app)


def main():
    import uvicorn
    from dotenv import load_dotenv
    from src.__infra__.env import get_env

    load_dotenv()
    server_host = get_env("SERVER_HOST")
    server_port = int(get_env("SERVER_PORT"))
    environment = get_env("ENVIRONMENT")
    is_local = environment.lower() == "local"
    if is_local:
        run_local_third_party_services()

    uvicorn.run(
        "main:app",
        host=server_host,
        port=server_port,
        reload=True if is_local else False,
        reload_excludes=["logs/*", "temp/*"]
    )


def run_local_third_party_services():
    from src.__infra__.elasticsearch import run_local_elasticsearch
    from src.__infra__.prefect import run_local_prefect
    perfect_info = run_local_prefect()
    elastic_info = run_local_elasticsearch()
    print(dedent(f"""
        ################################################################
        # {perfect_info}
        # {elastic_info}
        # Log file: third_party.txt
        ################################################################
        """))


if __name__ == "__main__":
    main()
