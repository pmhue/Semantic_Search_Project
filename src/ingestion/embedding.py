from threading import Lock
from typing import List

import torch
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from src.__infra__.env import get_env
from src.__infra__.logger import logger

load_dotenv()
model_name = get_env("EMBEDDING_MODEL")
model = None
model_lock = Lock()


def generate_embedding(content: str) -> List[float]:
    global model
    model = load_embedding_model()
    return model.encode(content).tolist()


def load_embedding_model():
    logger.info("Load embedding model")
    global model
    if model is None:
        with model_lock:
            device = (
                torch.device("mps")
                if torch.backends.mps.is_available()
                else torch.device("cuda")
                if torch.cuda.is_available()
                else torch.device("cpu")
            )
            model = SentenceTransformer(model_name)
            model = model.to(device)
    return model
