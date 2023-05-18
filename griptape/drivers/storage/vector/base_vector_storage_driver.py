from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from attr import define, field
from griptape.drivers import BaseEmbeddingDriver, OpenAiEmbeddingDriver


@define
class BaseVectorStorageDriver(ABC):
    @dataclass
    class QueryResult:
        vector: list[float]
        score: float
        meta: Optional[dict] = None
        namespace: Optional[str] = None

    embedding_driver: BaseEmbeddingDriver = field(
        default=OpenAiEmbeddingDriver(),
        kw_only=True
    )

    def insert_text(
            self,
            string: str,
            vector_id: Optional[str] = None,
            meta: Optional[dict] = None,
            **kwargs
    ) -> str:
        return self.insert_vector(
            self.embedding_driver.embed_string(string),
            vector_id=vector_id,
            meta=meta if meta else {},
            **kwargs
        )

    @abstractmethod
    def insert_vector(
            self,
            vector: list[float],
            vector_id: Optional[str] = None,
            meta: Optional[dict] = None,
            **kwargs
    ) -> str:
        ...

    @abstractmethod
    def query(self, query: str, **kwargs) -> list[QueryResult]:
        ...