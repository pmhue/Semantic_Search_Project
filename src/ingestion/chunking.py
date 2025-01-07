import re
from textwrap import dedent
from typing import List, Optional

import numpy as np
from prefect import task
from sentence_transformers import util

from src.ingestion.embedding import load_embedding_model


@task
def semantic_chunk(content: str) -> List[str]:
    return [content]


def semantic_chunk_v0(content: str, max_words: Optional[int] = 512) -> List[str]:
    """
    Chunk a document based on sentence boundaries and a maximum word count.

    Args:
        content (str): The text to be chunked into smaller segments.
        max_words (Optional[int]): The maximum number of words per chunk. Defaults to 512.

    Returns:
        List[str]: A list of text chunks, each containing up to `max_words` words.
    """
    sentences = re.split(r"(?<=[.!?])\s+", content)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        # Count words in the current sentence
        word_count = len(sentence.split())

        # If adding this sentence exceeds the max_words, start a new chunk
        if current_word_count + word_count > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = word_count
        else:
            current_chunk.append(sentence)
            current_word_count += word_count

    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def semantic_chunk_v1(content: str, method: Optional[str] = "percentile", threshold_value: Optional[float] = 90.0) -> List[str]:
    """
    Chunk a document into groups of similar sentences based on semantic similarity differences.

    Parameters:
    - content (str): The document to analyze.
    - method (str): The method to use for determining splits ("percentile", "std", "iqr").
    - threshold_value (float): The threshold value for the chosen method.

    Returns:
    - List[str]: A list of text chunks, each containing a group of similar sentences.
    """
    # Load the model
    model = load_embedding_model()

    # Split content into sentences
    sentences = re.split(r"(?<=[.!?])\s+", content)

    # Calculate embeddings for each sentence
    embeddings = model.encode(sentences)

    # Calculate pairwise cosine similarities
    similarities = [util.cos_sim(embeddings[i], embeddings[i + 1]).item() for i in range(len(embeddings) - 1)]

    # Calculate differences in similarities
    differences = np.diff(similarities)

    # Determine splits based on the chosen method
    # Percentile method
    if method == "percentile":
        threshold = np.percentile(differences, threshold_value)
    # Standard deviation method
    elif method == "std":
        mean_diff = np.mean(differences)
        std_diff = np.std(differences)
        threshold = mean_diff + 2 * std_diff
    # Inter quartile method
    elif method == "iqr":
        q1, q3 = np.percentile(differences, [25, 75])
        iqr = q3 - q1
        threshold = q3 + 1.5 * iqr
    else:
        raise ValueError("Method must be 'percentile', 'std', or 'iqr'.")

    # Find split indices
    split_indices = [j for j, diff in enumerate(differences) if diff > threshold]

    # Create chunks based on split indices
    chunks = []
    start_idx = 0
    for split_idx in split_indices:
        chunks.append(" ".join(sentences[start_idx:split_idx + 1]))
        start_idx = split_idx + 1
    # Add the last chunk
    chunks.append(" ".join(sentences[start_idx:]))

    return chunks


if __name__ == "__main__":
    # Example usage
    text_01 = dedent("""
        Artificial intelligence is transforming industries. Many companies are investing heavily in AI research. The potential applications of AI are vast, ranging from healthcare to finance. In healthcare, AI can help diagnose diseases more accurately. Financial institutions use AI to detect fraudulent transactions.
        Climate change is a pressing global issue. Scientists warn that immediate action is needed to mitigate its effects. Renewable energy sources like solar and wind are crucial in reducing carbon emissions. Governments worldwide are setting ambitious targets to transition to clean energy.
        The history of space exploration is fascinating. The first human landed on the moon in 1969. Since then, numerous missions have been launched to explore the solar system. Mars is a primary target for future exploration. Scientists are eager to find signs of past life on the red planet.
    """)

    print("---------------- semantic_chunk_v0 ----------------")
    for i, chunk in enumerate(semantic_chunk_v0(text_01, max_words=128)):
        print(f"Chunk {i + 1}:\n{chunk}\n")

    print("---------------- semantic_chunk_v1 ----------------")
    for i, chunk in enumerate(semantic_chunk_v1(text_01)):
        print(f"Chunk {i + 1}:\n{chunk}\n")
