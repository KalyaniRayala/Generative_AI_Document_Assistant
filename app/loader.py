from pathlib import Path

from app.document import Document
from app.services.text_cleaner import clean_text


def get_all_txt_files(folder_path: str) -> list[Path]:
    """
    Recursively find all .txt files inside the given folder.
    """

    folder = Path(folder_path)

    txt_files = list(folder.rglob("*.txt"))

    return txt_files


def read_txt_file(file_path: Path) -> str:
    """
    Read a text file and return its content.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_document(file_path: Path) -> Document:
    """
    Load a text file, clean it, and convert it into a Document object.
    """

    # Read the file
    content = read_txt_file(file_path)

    # Clean the text
    cleaned_content = clean_text(content)

    # Create and return a Document object
    return Document(
        file_name=file_path.name,
        file_path=str(file_path),
        content=cleaned_content,
    )


def load_all_documents(folder_path: str) -> list[Document]:
    """
    Load all text documents from the given folder.
    """

    files = get_all_txt_files(folder_path)

    documents = []

    for file in files:
        document = load_document(file)
        documents.append(document)

    return documents