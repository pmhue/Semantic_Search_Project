from datetime import datetime
from typing import List, Iterator

from dateutil.relativedelta import relativedelta
from unstructured.partition.auto import partition

from src.ingestion.connector.abstract_connector import Connector
from src.model import Document


class FileConnector(Connector):
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths

    def load_data(self) -> Iterator[Document]:
        for file_path in self.file_paths:
            try:
                elements = partition(file_path)
                content = "\n".join([element.text for element in elements if element.text])

                # Create a Passage object for each file
                yield Document(
                    doc_id=file_path,
                    content=content,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    effective_at=datetime.now(),
                    expired_at=datetime.now() + relativedelta(years=3)
                )
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
