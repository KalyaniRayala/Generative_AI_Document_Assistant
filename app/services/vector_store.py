import chromadb


class VectorStoreService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="django_docs"
        )

    def reset_collection(self):
        """
        Delete the existing collection and create a new one.
        This prevents duplicate embeddings when re-indexing.
        """

        try:
            self.client.delete_collection(
                name="django_docs"
            )

            print("✅ Old collection deleted.")

        except Exception:
            print("ℹ️ No existing collection found.")

        self.collection = self.client.get_or_create_collection(
            name="django_docs"
        )

        print("✅ New collection created.")

    def store_chunks(self, embedded_chunks):

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedded_chunks:

            import uuid

# inside the loop
            ids.append(str(uuid.uuid4()))

            documents.append(chunk.content)

            embeddings.append(chunk.embedding)

            metadatas.append(
                {
                    "file_name": chunk.file_name,
                    "file_path": chunk.file_path,
                    "source": chunk.source,
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"✅ Stored {len(ids)} chunks in ChromaDB.")