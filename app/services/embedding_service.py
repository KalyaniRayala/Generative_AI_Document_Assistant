from sentence_transformers import SentenceTransformer
from app.embedded_chunk import EmbeddedChunk


class EmbeddingService:

    _model = None

    def __init__(self):
        if EmbeddingService._model is None:
            EmbeddingService._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2",
                device="cpu"
            )

        self.model = EmbeddingService._model

    def generate_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return embedding.tolist()

    def embed_chunk(self, chunk):
        embedding = self.generate_embedding(chunk.content)

        return EmbeddedChunk(
            chunk_id=chunk.chunk_id,
            file_name=chunk.file_name,
            file_path=chunk.file_path,
            content=chunk.content,
            embedding=embedding,
            source=chunk.source,
        )