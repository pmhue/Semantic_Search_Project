import unittest

from src.ingestion.connector.huggingface_dataset_connector import HuggingFaceConnector
from src.model import Document


class TestHuggingFaceConnector(unittest.TestCase):
    def setUp(self):
        # Initialize the connector with the desired dataset and split
        self.connector = HuggingFaceConnector(
            dataset_path="microsoft/ms_marco",
            dataset_name="v1.1",
            split="train",
            max_size=10,
            chunk_size=5
        )

    def test_load_data(self):
        # Collect passages from the connector
        documents = []
        for document in self.connector.load_data():
            documents.append(document)

        # Validate that passages are returned
        self.assertGreater(len(documents), 0, "No passages were loaded.")
        for document in documents:
            self.assertIsInstance(document, Document, "The yielded object is not a Document instance.")
            self.assertIsNotNone(document.doc_id, "Document doc_id is None.")
            self.assertIsNotNone(document.content, "Document content is None.")
            self.assertIsNotNone(document.created_at, "Document created_at is None.")
            self.assertIsNotNone(document.updated_at, "Document updated_at is None.")
            self.assertIsNotNone(document.effective_at, "Document effective_at is None.")
            self.assertIsNotNone(document.expired_at, "Document expired_at is None.")


if __name__ == "__main__":
    unittest.main()
