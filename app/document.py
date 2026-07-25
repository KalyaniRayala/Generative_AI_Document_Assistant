from dataclasses import dataclass, field


@dataclass
class Document:
    """
    Represents a single documentation file.
    """

    file_name: str
    file_path: str
    content: str

    source: str = "django"
    document_type: str = "txt"

    metadata: dict = field(default_factory=dict)