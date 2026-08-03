import os
import tempfile

from app.document import Document
from app.services.pdf_loader import PDFLoader
from app.services.text_cleaner import clean_text
from app.services.chunker import create_sentence_chunks
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService


class IndexingService:

    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    # ==================================================
    # CHECK IF DOCUMENT ALREADY EXISTS
    # ==================================================

    def document_exists(self, file_name: str) -> bool:
        """
        Check whether a document with this file name
        already exists in ChromaDB.
        """

        try:
            results = self.vector_store.collection.get(
                where={
                    "file_name": file_name
                },
                limit=1
            )

            ids = results.get("ids", [])

            return len(ids) > 0

        except Exception as e:
            print(
                f"Error checking document existence: {e}"
            )

            return False

    # ==================================================
    # INDEX PDF
    # ==================================================

    def index_pdf_bytes(
        self,
        file_bytes: bytes,
        file_name: str
    ) -> int:
        """
        Index an uploaded PDF into ChromaDB.

        Returns:
            Number of chunks indexed.

            -1 means the document is already indexed.
             0 means no usable text was found.
            >0 means indexing succeeded.
        """

        # ----------------------------------------------
        # 1. Check for duplicate document
        # ----------------------------------------------

        if self.document_exists(file_name):

            print(
                f"⚠️ Document already indexed: {file_name}"
            )

            return -1

        temp_path = None

        try:

            # ------------------------------------------
            # 2. Create temporary PDF
            # ------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(file_bytes)

                temp_path = temp_file.name

            # ------------------------------------------
            # 3. Extract text
            # ------------------------------------------

            raw_text = self.pdf_loader.load_pdf(
                temp_path
            )

            # ------------------------------------------
            # 4. Validate text
            # ------------------------------------------

            if not raw_text or not raw_text.strip():
                return 0

            # ------------------------------------------
            # 5. Clean text
            # ------------------------------------------

            cleaned_text = clean_text(
                raw_text
            )

            if not cleaned_text.strip():
                return 0

            # ------------------------------------------
            # 6. Create Document object
            # ------------------------------------------

            document = Document(
                file_name=file_name,
                file_path=file_name,
                content=cleaned_text,
                source="uploaded_pdf",
                document_type="pdf"
            )

            # ------------------------------------------
            # 7. Create chunks
            # ------------------------------------------

            chunks = create_sentence_chunks(
                document,
                max_chunk_size=500
            )

            if not chunks:
                return 0

            # ------------------------------------------
            # 8. Generate embeddings
            # ------------------------------------------

            embedded_chunks = []

            for chunk in chunks:

                embedded_chunk = (
                    self.embedding_service.embed_chunk(
                        chunk
                    )
                )

                embedded_chunks.append(
                    embedded_chunk
                )

            # ------------------------------------------
            # 9. Store chunks in ChromaDB
            # ------------------------------------------

            self.vector_store.store_chunks(
                embedded_chunks
            )

            print(
                f"✅ Indexed {len(embedded_chunks)} "
                f"chunks from {file_name}"
            )

            # ------------------------------------------
            # 10. Return number of chunks
            # ------------------------------------------

            return len(embedded_chunks)

        finally:

            # ------------------------------------------
            # 11. Delete temporary PDF
            # ------------------------------------------

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                os.remove(temp_path)