from app.loader import load_all_documents
from app.services.chunker import(
    create_fixed_chunks,
    create_overlapping_chunks,
    create_sentence_chunks,
    create_token_chunks,
)

def main():

    documents = load_all_documents("data/django")

    document=documents[0]

    fixed_chunks=create_fixed_chunks(document)
    overlap_chunks=create_overlapping_chunks(document)
    sentence_chunks=create_sentence_chunks(document)
    token_chunks=create_token_chunks(document)
    print("=" * 60)

    print("Fixed Chunks :", len(fixed_chunks))
    print("overlapping Chunks :", len(overlap_chunks))
    print("sentence Chunks :", len(sentence_chunks))
    print("token Chunks :", len(token_chunks))

    print("=" * 60)
    print("\n First fixed chunk\n")
    print(fixed_chunks[0].content)

    print("\n" + "=" *60)

    print("\n First overlapping chunk\n")
    print(overlap_chunks[0].content)

    print("\n" + "=" *60)
    print("\n First Sentence Chunks\n")
    print(sentence_chunks[0].content)

    print("\n" + "=" *60)
    print("\nFirst Token Chunks\n")
    print(token_chunks[0].content)

if __name__ == "__main__":
    main()