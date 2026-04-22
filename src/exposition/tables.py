from dataclasses import dataclass, field


@dataclass
class Table:
    database: str
    schema: str
    name: str
    columns: list[str] = field(default_factory=lambda: ["*"])
