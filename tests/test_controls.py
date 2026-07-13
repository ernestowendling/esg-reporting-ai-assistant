"""Control-focused tests for the public MVP."""

from pathlib import Path

from src.assistant import REFUSAL_TEXT, answer_question
from src.documents import load_evidence
from src.retrieval import EvidenceRetriever


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_retriever() -> EvidenceRetriever:
    return EvidenceRetriever(load_evidence(DATA_DIR))


def test_supported_metric_retrieves_exact_csv_row() -> None:
    results = build_retriever().retrieve(
        "What was the financed emissions intensity in 2025?", top_k=4
    )
    assert results
    assert results[0].chunk.source == "esg_metrics.csv"
    assert "value=72.0" in results[0].chunk.text


def test_unsupported_question_triggers_no_evidence_refusal() -> None:
    results = build_retriever().retrieve(
        "What was the fund's water consumption in 2025?", top_k=4
    )
    answer, model, review_required = answer_question(
        question="What was the fund's water consumption in 2025?",
        results=results,
        minimum_score=0.20,
        api_key=None,
    )
    assert answer == REFUSAL_TEXT
    assert model == "guardrail"
    assert review_required is True


def test_demo_mode_keeps_source_citations() -> None:
    results = build_retriever().retrieve(
        "Which principal adverse impact indicator exceeded its threshold?", top_k=4
    )
    answer, model, _ = answer_question(
        question="Which principal adverse impact indicator exceeded its threshold?",
        results=results,
        minimum_score=0.20,
        api_key=None,
    )
    assert model == "extractive-demo"
    assert results[0].chunk.citation in answer
