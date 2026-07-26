from app.chunk import Chunk
def create_fixed_chunks(document, chunk_size=500):

    """
    Split one document into fixed-size chunks.
    """

    chunks = []

    content = document.content

    for start in range(0, len(content), chunk_size):

        end = start + chunk_size

        chunk_text = content[start:end]

        chunk = Chunk(
            chunk_id=len(chunks) + 1,
            file_name=document.file_name,
            file_path=document.file_path,
            content=chunk_text,
        )

        chunks.append(chunk)

    return chunks


def create_overlapping_chunks(document, chunk_size=500, overlap=100):

    """Split the document into overlapping chunks."""

    chunks = []

    content = document.content

    start = 0

    chunk_id = 1

    while start < len(content):

        end = start + chunk_size

        chunk = Chunk(
            chunk_id=chunk_id,
            file_name=document.file_name,
            file_path=document.file_path,
            content=content[start:end],
        )

        chunks.append(chunk)

        start += chunk_size - overlap

        chunk_id += 1

    return chunks


def create_sentence_chunks(document, max_chunk_size=500):

    chunks=[]
    sentence=document.content.split(". ")
    current_chunk=""
    chunk_id=1
    for sentence in sentence:
        sentence=sentence.strip()
        if not sentence:
             continue
        sentence+=". "
        if len(current_chunk) + len(sentence) <= max_chunk_size:

            current_chunk += sentence

        else:

            chunk = Chunk(
                chunk_id=chunk_id,
                file_name=document.file_name,
                file_path=document.file_path,
                content=current_chunk.strip(),
                source=document.source
            )

            chunks.append(chunk)

            chunk_id += 1

            current_chunk = sentence

    if current_chunk:

        chunk = Chunk(
            chunk_id=chunk_id,
            file_name=document.file_name,
            file_path=document.file_path,
            content=current_chunk.strip(),
            source=document.source
        )

        chunks.append(chunk)

    return chunks
def create_token_chunks(document, token_size=500):
    """
    Simulated token-based chunking.
    (Currently uses words as tokens.)
    """

    chunks = []

    words = document.content.split()

    chunk_id = 1

    for start in range(0, len(words), token_size):

        end = start + token_size

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunk = Chunk(
            chunk_id=chunk_id,
            file_name=document.file_name,
            file_path=document.file_path,
            content=chunk_text,
            source=document.source
        )

        chunks.append(chunk)

        chunk_id += 1

    return chunks


