import chromadb

from app.services.embedding_service import EmbeddingService


class RetrieverService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_collection(
            name="django_docs"
        )

        self.embedding_service = EmbeddingService()

    def search(self, query: str, n_results: int = 3):

        query_embedding = self.embedding_service.generate_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        return results