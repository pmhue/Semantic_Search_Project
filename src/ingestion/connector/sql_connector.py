from datetime import datetime
from typing import AsyncIterator

import asyncpg
from dateutil.relativedelta import relativedelta

from src.ingestion.connector.abstract_connector import Connector
from src.model import Document


class SQLConnector(Connector):
    def __init__(self, connection_string: str, query: str):
        self.connection_string = connection_string
        self.query = query

    async def load_data(self) -> AsyncIterator[Document]:
        conn = await asyncpg.connect(self.connection_string)
        async with conn.transaction():
            async for record in conn.cursor(self.query):
                yield Document(
                    doc_id=record['doc_id'],
                    content=record['content'],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    effective_at=datetime.now(),
                    expired_at=datetime.now() + relativedelta(years=3)
                )
        await conn.close()
