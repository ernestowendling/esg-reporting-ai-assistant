"""SQLite evidence log for reproducible, auditable prototype interactions."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

import pandas as pd

from .retrieval import RetrievalResult


SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc TEXT NOT NULL,
    question TEXT NOT NULL,
    status TEXT NOT NULL,
    model TEXT NOT NULL,
    top_retrieval_score REAL NOT NULL,
    sources_json TEXT NOT NULL,
    answer TEXT NOT NULL,
    human_review_required INTEGER NOT NULL
);
"""


def initialise_database(database_path: Path) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(SCHEMA)
        connection.commit()


def log_interaction(
    database_path: Path,
    question: str,
    answer: str,
    model: str,
    results: list[RetrievalResult],
    human_review_required: bool,
) -> None:
    initialise_database(database_path)
    top_score = results[0].score if results else 0.0
    status = "refused" if answer.startswith("INSUFFICIENT EVIDENCE:") else "answered"
    sources = [
        {
            "citation": result.chunk.citation,
            "score": round(result.score, 4),
        }
        for result in results
    ]
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO evidence_log (
                timestamp_utc, question, status, model, top_retrieval_score,
                sources_json, answer, human_review_required
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                question,
                status,
                model,
                top_score,
                json.dumps(sources),
                answer,
                int(human_review_required),
            ),
        )
        connection.commit()


def read_log(database_path: Path) -> pd.DataFrame:
    initialise_database(database_path)
    with sqlite3.connect(database_path) as connection:
        return pd.read_sql_query(
            "SELECT * FROM evidence_log ORDER BY id DESC",
            connection,
        )
