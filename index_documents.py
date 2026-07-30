from app.loader import load_all_documents
from app.services.chunker import create_sentence_chunks
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService


def main():

    print("=" * 60)
    print("📄 Document Indexer")
    print("=" * 60)

    documents = load_all_documents("data")

    print(f"\nFound {len(documents)} document(s).\n")

    embedding_service = EmbeddingService()

    vector_store = VectorStoreService()

    # Reset old database
    vector_store.reset_collection()

    all_embedded_chunks = []

    for document in documents:

        print(f"📄 Processing: {document.file_name}")

        chunks = create_sentence_chunks(document)

        print(f"   Created {len(chunks)} chunks")

        for chunk in chunks:

            embedded_chunk = embedding_service.embed_chunk(chunk)

            all_embedded_chunks.append(embedded_chunk)

    print(f"\nTotal Embedded Chunks: {len(all_embedded_chunks)}")

    vector_store.store_chunks(all_embedded_chunks)

    print("\n🎉 Indexing Completed Successfully!")


if __name__ == "__main__":
    main()