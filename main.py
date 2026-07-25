from app.loader import load_all_documents


def main():

    documents = load_all_documents("data/django")

    print("=" * 60)
    print(f"Total Documents Loaded : {len(documents)}")
    print("=" * 60)

    first_document = documents[0]

    print("\nFile Name:")
    print(first_document.file_name)

    print("\nFile Path:")
    print(first_document.file_path)

    print("\nDocument Type:")
    print(first_document.document_type)

    print("\nSource:")
    print(first_document.source)

    print("\nContent Preview:\n")
    print(first_document.content[:1000])


if __name__ == "__main__":
    main()