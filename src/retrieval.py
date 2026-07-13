"""Transparent lexical retrieval for the first public MVP.

This is a deliberately lightweight RAG retriever based on TF-IDF and cosine
similarity. It is easy to inspect and deploy. The roadmap replaces this layer
with embeddings and a vector database while preserving the same evidence
contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .documents import EvidenceChunk


@dataclass(frozen=True)
class RetrievalResult:
    chunk: EvidenceChunk
    score: float


class EvidenceRetriever:
    """Rank evidence chunks against a user question."""

    def __init__(self, chunks: list[EvidenceChunk]) -> None:
        if not chunks:
            raise ValueError("At least one evidence chunk is required.")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform(chunk.text for chunk in chunks)

    def retrieve(self, question: str, top_k: int = 4) -> list[RetrievalResult]:
        if not question.strip():
            return []
        question_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(question_vector, self.matrix).flatten()
        ranked_indexes = scores.argsort()[::-1][:top_k]
        return [
            RetrievalResult(chunk=self.chunks[index], score=float(scores[index]))
            for index in ranked_indexes
            if scores[index] > 0
        ]
