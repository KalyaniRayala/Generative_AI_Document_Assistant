from app.loader import load_all_documents


from app.services.chunker import (
    create_fixed_chunks,
    create_overlapping_chunks,
    create_sentence_chunks,
    create_token_chunks,
)

from app.services.embedding_service import EmbeddingService


def main():

    # Load documents
    documents = load_all_documents("data/django")

    # Select first document
    document = documents[0]

    # Create chunks
    fixed_chunks = create_fixed_chunks(document)
    overlap_chunks = create_overlapping_chunks(document)
    sentence_chunks = create_sentence_chunks(document)
    token_chunks = create_token_chunks(document)

    # Load embedding model
    embedding_service = EmbeddingService()

    # Generate embeddings for all fixed chunks
    embedded_chunks = []

    for chunk in fixed_chunks:
        embedded_chunk = embedding_service.embed_chunk(chunk)
        embedded_chunks.append(embedded_chunk)

    print("=" * 60)
    print("Fixed Chunks       :", len(fixed_chunks))
    print("Overlapping Chunks :", len(overlap_chunks))
    print("Sentence Chunks    :", len(sentence_chunks))
    print("Token Chunks       :", len(token_chunks))
    print("Embedded Chunks    :", len(embedded_chunks))
    print("=" * 60)

    print()
    print("First Embedded Chunk")
    print()
    print(embedded_chunks[0])


if __name__ == "__main__":
    main()