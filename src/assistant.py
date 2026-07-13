"""Grounded answer generation with an explicit no-evidence guardrail."""

from __future__ import annotations

import os
from typing import Iterable

from .retrieval import RetrievalResult

REFUSAL_TEXT = (
    "INSUFFICIENT EVIDENCE: the available synthetic source documents do not "
    "support a reliable answer. A human reviewer should obtain additional evidence."
)


def _format_context(results: Iterable[RetrievalResult]) -> str:
    blocks = []
    for result in results:
        blocks.append(
            f"CITATION: {result.chunk.citation}\n"
            f"RETRIEVAL_SCORE: {result.score:.3f}\n"
            f"EVIDENCE: {result.chunk.text}"
        )
    return "\n\n".join(blocks)


def _extractive_demo_answer(question: str, results: list[RetrievalResult]) -> str:
    """Provide a safe demo when no paid API key is configured."""
    evidence_lines = "\n\n".join(
        f"- {result.chunk.text} {result.chunk.citation}" for result in results[:3]
    )
    return (
        "**Demo mode — retrieved evidence only**\n\n"
        f"For the question *{question}*, the strongest available evidence is:\n\n"
        f"{evidence_lines}\n\n"
        "This extractive response has not been rewritten by an LLM and requires human review."
    )


def answer_question(
    question: str,
    results: list[RetrievalResult],
    minimum_score: float,
    api_key: str | None = None,
    model: str | None = None,
) -> tuple[str, str, bool]:
    """Return answer, model label and whether human review is required."""
    top_score = results[0].score if results else 0.0
    if not results or top_score < minimum_score:
        return REFUSAL_TEXT, "guardrail", True

    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

    if not api_key:
        return _extractive_demo_answer(question, results), "extractive-demo", True

    system_prompt = """You are an ESG reporting assistant operating in a regulated environment.
Use ONLY the supplied evidence. Do not use external knowledge or fill gaps.
Every substantive factual claim must include one or more of the supplied citation labels exactly.
If the evidence is insufficient or conflicting, start with 'INSUFFICIENT EVIDENCE:' and explain what is missing.
Write a concise, professional draft for human review. Never claim that the output is final or legally approved."""

    user_prompt = f"""QUESTION:
{question}

RETRIEVED EVIDENCE:
{_format_context(results)}

Produce a grounded answer with exact citations and finish with: 'Human review required.'"""

    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=700,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    answer = "".join(
        block.text for block in message.content if getattr(block, "type", "") == "text"
    ).strip()

    supplied_citations = [result.chunk.citation for result in results]
    has_valid_citation = any(citation in answer for citation in supplied_citations)
    if not has_valid_citation:
        return (
            "INSUFFICIENT EVIDENCE: the model response failed the citation validation control. "
            "A human reviewer must inspect the retrieved evidence.",
            model,
            True,
        )
    return answer, model, True
