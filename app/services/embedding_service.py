from sentence_transformers import SentenceTransformer
from app.embedded_chunk import EmbeddedChunk

class EmbeddingService:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.
        """

        embedding = self.model.encode(text)

        return embedding.tolist()

    def embed_chunk(self, chunk):
        """
        Convert one Chunk object into one EmbeddedChunk object.
        """

        embedding = self.generate_embedding(chunk.content)

        embedded_chunk = EmbeddedChunk(
            chunk_id=chunk.chunk_id,
            file_name=chunk.file_name,
            file_path=chunk.file_path,
            content=chunk.content,
            embedding=embedding,
            source=chunk.source,
        )

        return embedded_chunk