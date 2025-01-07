# Semantic Search Thesis

## Overview

The Semantic Search project aims to enhance traditional search capabilities by incorporating semantic understanding, allowing for more accurate and context-aware retrieval of information. This system is designed to process and index large volumes of data, enabling efficient and meaningful search results.

- [Semantic Search Thesis](#semantic-search-thesis)
    - [Overview](#overview)
    - [Components](#components)
        - [1. Data Ingestion Pipeline](#1-data-ingestion-pipeline)
        - [2. Search Pipeline](#2-search-pipeline)
        - [3. Evaluation](#3-evaluation)
        - [4. Query Classification](#4-query-classification)
        - [5. Workflow Orchestration](#5-workflow-orchestration)
        - [6. Data Storage](#6-data-storage)
    - [Project Overview](#project-overview)
        - [Project Structure](#project-structure)
        - [Prerequisite](#prerequisite)
        - [Install Dependency](#install-dependency)
        - [Run Project](#run-project)
        - [Test Project](#test-project)
    - [Comparison between Approaches](#comparison-between-approaches)
        - [1. Search](#1-search)
        - [2. Store Embedding](#2-store-embedding)
        - [3. Metrics](#3-metrics)
        - [4. Search Strategy](#4-search-strategy)
    - [Expansion](#expansion)

## Components

### 1. Data Ingestion Pipeline

The data ingestion pipeline is crucial for sourcing and preparing raw data for semantic search. It involves several key processes:

- **Connectors**: These are specialized modules designed to interface with various data sources. Current connectors include:
    - **Hugging Face Dataset Connector**: Retrieves data directly from Hugging Face datasets, allowing seamless integration with a wide range of pre-existing datasets.
    - **SQL Connector**: Extracts data from SQL databases, enabling the system to access structured data stored in relational databases.
    - **File Connector**: Handles data extraction from local or cloud-based file systems, supporting formats like CSV, JSON, and more.

- **Data Extraction**: Once data is retrieved via connectors, it is transformed into a standardized Document structure. This structure facilitates consistent processing and indexing across different data types and sources.

- **Semantic Chunking**: The Document structure is divided into smaller, semantically meaningful chunks. This granularity enhances the system's ability to process and index data accurately, improving search result precision.

- **Embedding Generation**: Each chunk of text is converted into a vector representation using advanced embedding techniques (e.g., [Sentence Transformer - paraphrase-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2)). These embeddings capture the semantic meaning of the text, enabling the system to understand context and relationships between different pieces of information.

- **Indexing**:
    - **Inverted Index**: A traditional indexing method that maps keywords to their locations in the document set, allowing for quick keyword-based searches.
    - **Semantic Index**: This index uses semantic embeddings to map queries to relevant document chunks based on meaning rather than just keywords.

### 2. Search Pipeline

The search pipeline integrates both the `Inverted Index` and `Semantic Index` to efficiently retrieve relevant documents, allowing users to select from various strategies to enhance search accuracy and relevance.

- **Hybrid Search**:
    - **Inverted Index**: Quickly filters documents using keyword matching for straightforward queries.
    - **Semantic Index**: Reranks results by understanding query context and meaning for more relevant documents.

- **Fallback Mechanism**:
    - **Semantic Index First**: Prioritizes high relevance and contextual understanding.
    - **Fallback to Inverted Index**: Switches to keyword-based search if needed.

- **Tiered Search**:
    - Classify queries as simple or complex.
    - **Inverted Index**: Used for simple queries with keyword matching.
    - **Semantic Index**: Used for complex queries to capture user intent and provide precise results.

Search Diagram

![search-diagram](docs/semantic-search-diagram-20250103.png)

### 3. Evaluation

The system's performance is evaluated using the [MS MARCO dataset](https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train), a benchmark for machine reading comprehension and passage ranking:

- **MS MARCO Dataset**: Contains real user queries and associated passages, providing a realistic testbed for evaluating search systems.

- **Metrics Calculation**:
    - **Precision@k**: Measures the proportion of relevant documents in the top `k` results, indicating the system's ability to prioritize relevant information.
    - **MRR@10 (Mean Reciprocal Rank at 10)**: Evaluates the ranking quality by considering the position of the first relevant document in the top 10 results.

### 4. Query Classification

In the `Tiered Search` approach, accurately distinguishing between simple and complex queries is crucial for enhancing search precision. Using the [MS MARCO dataset](https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train), queries are classified based on the `query_type` column:

- **Simple Queries**: Labeled as `description`.
- **Complex Queries**: Include `entity`,   `location`,   `numeric`, and other types.

**Methodology**:

- **Data Preparation**: Tokenize and embed queries using the `paraphrase-mpnet-base-v2` model's tokenizer.
- **Model Training**: Fine-tune a sequence classification model to predict binary labels, distinguishing between simple and complex queries.
- **Evaluation**: Assess model performance using the test set from the MS MARCO dataset.

**Results**:

- The model effectively classifies query complexity using semantic embeddings, enhancing the tiered search system.

### 5. Workflow Orchestration

The system uses [Prefect](https://www.prefect.io/) for managing workflows, ensuring efficient and reliable execution of tasks:

- **Flow**: Represents the overall process, including data ingestion, search, and feedback loops.
- **Task**: Individual components of the flow, such as semantic chunking, embedding generation, query expansion, and query classification.

### 6. Data Storage

Efficient data storage solutions are employed to handle both raw and processed data:

- **Raw Documents Storage**: [MongoDB](https://www.mongodb.com/) is used to store unprocessed documents, providing a scalable and flexible database solution.
- **Processed Data Storage**: [Elasticsearch](https://www.elastic.co/elasticsearch) is used for storing processed and indexed data, enabling fast and efficient search operations.

## Project Overview

### Project Structure

```plaintext
semantic-search/
│
├── data/
│   ├── raw/                     # Raw documents
│   ├── processed/               # Processed and chunked documents
│
├── src/
│   ├── __init__.py
│   ├── ingest.py                # Ingest flow
│   ├── chunking.py              # Semantic chunking
│   ├── embedding.py             # Embedding generation
│   ├── search.py                # Hybrid search logic
│   ├── query_expansion.py       # Query expansion logic
│   ├── query_classification.py  # Query classification logic
│   ├── evaluation.py            # Evaluation metrics
│   ├── database.py              # Database interaction
│   ├── flow.py                  # Prefect flow
│
├── requirements.txt             # Python dependencies
├── main.py                      # Main entry point
└── README.md
```

### Prerequisite

- **Docker**: Required to run third-party services such as Elasticsearch and Postgres.
- **Python version**: 3.12

### Install Dependency

To set up the project environment, run the following script:

```bash
bash scripts/setup.sh
```

### Run Project

To start the project, execute:

```bash
bash scripts/start.sh
```

### Test Project

To test the project's functionality, use:

```bash
bash scripts/test.sh
```

## Comparison between Approaches

This project evaluates various search and indexing methods, highlighting their advantages and disadvantages

### 1. Search

- **Elastic Search**: Supports complex ranking and CRUD operations, ideal for large-scale applications. Allows for distributed storage, aiding in scaling.
- **FAISS**: Offers fast in-memory processing, perfect for efficiently handling large datasets, but lacks CRUD support and persistent storage.
- **TF-IDF**: Simple to implement but slow for large datasets due to run-time computation.

### 2. Store Embedding

- **Vector Database**:  Optimized for storing and querying high-dimensional vectors, providing efficient similarity search.
- **Elastic-Search KNN-plugin**: Integrates seamlessly with existing Elastic Search setups, enabling efficient k-nearest neighbor searches.

### 3. Metrics

- **Precision@k, MRR@10**: Focuses on the accuracy and ranking quality of the first few results, crucial for applications like chatbots where the first response is often the most important.
- **Recall@k**: Measures the ability to retrieve all relevant documents within the top k results, highlighting the system's comprehensiveness.
- **F1-Score**: Balances precision and recall, providing a single metric to evaluate overall search performance.

### 4. Search Strategy

- **Hybrid Search**: This approach optimizes cost by initially filtering results using keyword search before applying semantic ranking. However, its limitation lies in the potential failure of keyword search to handle complex queries, which can result in insufficient data for effective ranking.
- **Tiered Search**: Balances efficiency and accuracy by categorizing queries into simple and complex types, applying keyword search for straightforward queries and semantic search for more intricate ones.
- **Fallback Mechanism**: Prioritizes high accuracy by starting with semantic search, but this can be computationally expensive. If semantic search does not yield satisfactory results, it falls back to keyword-based methods to ensure comprehensive search coverage.

## Expansion

The project outlines potential areas for expansion and improvement:

- **Connectors**: Develop additional connectors to integrate with various data sources.
- **Human Feedback**: Incorporate user feedback to improve search accuracy and relevance.
- **Complex Ranking**:
    - Enhance ranking algorithms by incorporating factors like semantics, issuance date, effective date, and applicable subjects.
    - Utilize Elasticsearch's built-in semantic search with cross-encoder for improved relevance.
- **Accelerating Processing on GPU**:
    - Utilize GPUs to enhance processing speed.
    - Perform similarity calculations in Elasticsearch using the CPU by default.
- **Real-life Applications**: Employ semantic search to aggregate data from `diverse sources`, improving user interaction across domains:
    - **Requirement Analysis**: Improve the integration and understanding of business, product, and technical requirements.
    - **Customer Support**: Accurately match user inquiries with solutions by understanding the semantics of queries.
    - **Legal Analysis**: Enable efficient search and contextual analysis of legal documents.
