import os
import signal

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from testcontainers.elasticsearch import ElasticSearchContainer

from src.__infra__.env import get_env

load_dotenv()
local_directory = os.path.abspath("data/elasticsearch")
container_directory = "/usr/share/elasticsearch/data"


def run_local_elasticsearch():
    print("Starting Elasticsearch container...")
    es = ElasticSearchContainer("elasticsearch:8.17.0")
    es.with_env("discovery.type", "single-node")
    es.with_env("cluster.routing.allocation.disk.threshold_enabled", "false")
    es.with_volume_mapping(local_directory, container_directory, mode="rw")

    es.start()

    es_url = es.get_url()
    server_info = f"Elasticsearch: {es_url}"
    print(server_info)
    os.environ['ELASTIC_ENDPOINT'] = es_url
    with open("third_party.txt", "a") as file:
        file.write(f"{server_info}\n")

    def signal_handler(sig, frame):
        print('Stopping the Elasticsearch container...')
        es.stop()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    return server_info


def get_elasticsearch_client():
    return Elasticsearch(
        hosts=[get_env("ELASTIC_ENDPOINT")],
    )
