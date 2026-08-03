import os
from app.services.pdf_loader import PDFLoader
from app.services.chunker import chunk_documents
from app.services.vector_store import VectorStore

class PDFProcessor:

    def __init__(self):
        self.loader = PDFLoader()
        self.vector_store = VectorStore()

    def process(self, pdf_path):

        documents = self.loader.load_pdf(pdf_path)

        chunks = chunk_documents(documents)

        self.vector_store.store_documents(chunks)

        return len(chunks)