from dataclasses import dataclass, field


@dataclass
class Chunk:
    """
    Represents one chunk of a document.
    """

    chunk_id: int

    file_name: str

    file_path: str

    content: str

    source: str = "django"

    metadata: dict = field(default_factory=dict)