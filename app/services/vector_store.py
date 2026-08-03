import uuid
import chromadb


class VectorStoreService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="django_docs"
        )

    # ==================================================
    # RESET ENTIRE COLLECTION
    # ==================================================

    def reset_collection(self):
        """
        Delete the entire ChromaDB collection
        and create a new empty collection.

        WARNING:
        This removes ALL indexed documents.
        """

        try:

            self.client.delete_collection(
                name="django_docs"
            )

            print("✅ Old collection deleted.")

        except Exception:

            print("ℹ️ No existing collection found.")

        self.collection = (
            self.client.get_or_create_collection(
                name="django_docs"
            )
        )

        print("✅ New collection created.")

    # ==================================================
    # STORE EMBEDDED CHUNKS
    # ==================================================

    def store_chunks(self, embedded_chunks):

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedded_chunks:

            # Generate unique ChromaDB ID
            ids.append(
                str(uuid.uuid4())
            )

            documents.append(
                chunk.content
            )

            embeddings.append(
                chunk.embedding
            )

            metadatas.append(
                {
                    "file_name": chunk.file_name,
                    "file_path": chunk.file_path,
                    "source": chunk.source,
                }
            )

        if not ids:

            print(
                "ℹ️ No chunks to store."
            )

            return

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(
            f"✅ Stored {len(ids)} chunks "
            "in ChromaDB."
        )

    # ==================================================
    # CHECK IF DOCUMENT EXISTS
    # ==================================================

    def document_exists(
        self,
        file_name: str
    ) -> bool:
        """
        Check whether a document exists
        in ChromaDB using its file name.
        """

        try:

            result = self.collection.get(
                where={
                    "file_name": file_name
                },
                limit=1
            )

            ids = result.get(
                "ids",
                []
            )

            return len(ids) > 0

        except Exception as e:

            print(
                f"Error checking document: {e}"
            )

            return False

       # ==================================================
    # DELETE ONE DOCUMENT
    # ==================================================

        # ==================================================
    # DELETE ONE DOCUMENT
    # ==================================================

    def delete_document(
        self,
        file_name: str
    ) -> int:
        """
        Delete all chunks belonging to one document
        from ChromaDB.

        Returns the number of deleted chunks.
        """

        try:
            # Find all chunks for this file
            result = self.collection.get(
                where={
                    "file_name": file_name
                }
            )

            ids = result.get("ids", [])

            # Nothing found
            if not ids:
                print(
                    f"ℹ️ Document not found: {file_name}"
                )
                return 0

            # Delete the matching chunks
            self.collection.delete(
                ids=ids
            )

            print(
                f"✅ Deleted {len(ids)} chunks "
                f"from {file_name}"
            )

            return len(ids)

        except Exception as e:
            print(
                f"❌ Error deleting document: {e}"
            )
            raise

        try:
            # Find all chunks for this file
            result = self.collection.get(
                where={
                    "file_name": file_name
                }
            )

            ids = result.get("ids", [])

            # Nothing found
            if not ids:
                print(
                    f"ℹ️ Document not found: {file_name}"
                )
                return 0

            # Delete the matching chunks
            self.collection.delete(
                ids=ids
            )

            print(
                f"✅ Deleted {len(ids)} chunks "
                f"from {file_name}"
            )

            return len(ids)

        except Exception as e:
            print(
                f"❌ Error deleting document: {e}"
            )
            raise