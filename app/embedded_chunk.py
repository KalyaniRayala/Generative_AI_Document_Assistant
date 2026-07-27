from dataclasses import dataclass, field



@dataclass
class EmbeddedChunk:
    """
    Stores one chunk together with its embedding vector.
    """

    chunk_id: int

    file_name: str

    file_path: str

    content: str

    embedding: list[float]

    source: str = "django"

    metadata: dict = field(default_factory=dict)