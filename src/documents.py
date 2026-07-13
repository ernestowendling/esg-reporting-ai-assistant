"""Load and chunk synthetic ESG source documents.

The prototype deliberately keeps document processing simple and transparent.
Each chunk retains source metadata so every generated answer can be traced back
through the evidence log.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import pandas as pd


@dataclass(frozen=True)
class EvidenceChunk:
    """A retrievable piece of evidence with audit-friendly metadata."""

    chunk_id: str
    source: str
    location: str
    text: str

    @property
    def citation(self) -> str:
        return f"[{self.source} | {self.location} | {self.chunk_id}]"


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _load_markdown(path: Path) -> list[EvidenceChunk]:
    """Split Markdown into heading-aware paragraphs."""
    chunks: list[EvidenceChunk] = []
    current_heading = "Document introduction"
    buffer: list[str] = []
    chunk_number = 1

    def flush() -> None:
        nonlocal chunk_number
        text = _clean_text(" ".join(buffer))
        if text:
            chunks.append(
                EvidenceChunk(
                    chunk_id=f"chunk-{chunk_number}",
                    source=path.name,
                    location=f"section: {current_heading}",
                    text=text,
                )
            )
            chunk_number += 1
        buffer.clear()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            flush()
            current_heading = line.lstrip("#").strip()
        elif not line:
            flush()
        else:
            buffer.append(line)
    flush()
    return chunks


def _load_csv(path: Path) -> list[EvidenceChunk]:
    """Convert each synthetic metric row into a citable evidence chunk."""
    frame = pd.read_csv(path)
    chunks: list[EvidenceChunk] = []
    for row_number, row in frame.iterrows():
        pairs = [f"{column}={row[column]}" for column in frame.columns]
        chunks.append(
            EvidenceChunk(
                chunk_id=f"row-{row_number + 2}",  # +2 accounts for header and zero index
                source=path.name,
                location=f"CSV row {row_number + 2}",
                text="; ".join(pairs),
            )
        )
    return chunks


def load_evidence(data_directory: Path) -> list[EvidenceChunk]:
    """Load supported synthetic evidence files from the data directory."""
    chunks: list[EvidenceChunk] = []
    for path in sorted(data_directory.rglob("*")):
        if path.suffix.lower() == ".md":
            chunks.extend(_load_markdown(path))
        elif path.suffix.lower() == ".csv":
            chunks.extend(_load_csv(path))
    if not chunks:
        raise FileNotFoundError(f"No .md or .csv evidence found in {data_directory}")
    return chunks
