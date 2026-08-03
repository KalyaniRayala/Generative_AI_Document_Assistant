import chromadb

from app.services.embedding_service import EmbeddingService


class RetrieverService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="django_docs"
        )

        self.embedding_service = EmbeddingService()

        # -----------------------------------------
    # Search documents
    # -----------------------------------------
    def search(
        self,
        query: str,
        n_results: int = 3,
        file_name: str | None = None
    ):

        # Prevent empty queries
        if not query or not query.strip():
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }

        # Convert question into embedding
        query_embedding = (
            self.embedding_service.generate_embedding(
                query.strip()
            )
        )

        query_args = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,

            # Important for accuracy checking
            "include": [
                "documents",
                "metadatas",
                "distances"
            ]
        }

        # If user selected one document,
        # search only inside that document
        if file_name:
            query_args["where"] = {
                "file_name": file_name
            }

        results = self.collection.query(
            **query_args
        )

        return results

    # -----------------------------------------
    # Get all indexed document names
    # -----------------------------------------
    def get_indexed_files(self):

        try:

            results = self.collection.get(
                include=["metadatas"]
            )

            metadatas = results.get("metadatas", [])

            file_names = set()

            for metadata in metadatas:

                if metadata and metadata.get("file_name"):
                    file_names.add(
                        metadata["file_name"]
                    )

            return sorted(file_names)

        except Exception as e:

            print(
                f"Error getting indexed files: {e}"
            )

            return []