from src.__infra__.logger import logger
from src.model import SearchFeedbackInput


def human_feedback(feedback: SearchFeedbackInput) -> None:
    logger.info(f"Feedback: {feedback}")
    # TODO
