# ESG Reporting AI Assistant

A synthetic ESG document-retrieval prototype with source references, an extractive demonstration mode and optional LLM-generated drafts for human review.

## Implemented today

- Load the bundled synthetic evidence and rank passages with TF-IDF and cosine similarity.
- Display retrieved passages, source references and relevance scores.
- Refuse when no evidence is retrieved or the best score falls below the configured threshold.
- Return retrieved excerpts without a paid API key.
- Optionally use the Anthropic API to draft an answer from retrieved passages.
- Reject an LLM response when it contains none of the supplied citation labels.
- Record interactions in a local SQLite evidence log, with CSV export in the interface.

Citation presence does not establish that every claim is supported. The retrieval threshold measures lexical similarity, not factual correctness or evidence sufficiency. Every output requires human review.

## Run locally

```bash
git clone https://github.com/ernestowendling/esg-reporting-ai-assistant.git
cd esg-reporting-ai-assistant
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on macOS/Linux.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

No API key is needed for extractive demo mode. For optional generated drafts, copy `.env.example` to a local `.env` and configure `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` for a model available to your account. The app loads dotenv and also accepts Streamlit secrets, which take precedence. Keep credentials outside version control.

## Review the demonstration

1. Select “What was the fund's financed-emissions intensity in 2025?” and inspect the returned passages against the bundled synthetic data.
2. Try an unrelated query such as “quantum teleportation qubits” to exercise the no-evidence path.
3. Review source references and the evidence log. Do not treat a high retrieval score as proof that an answer is supported.

These are reproducible review scenarios, not reported evaluation results.

## Project structure

- `app.py`: Streamlit interface and workflow coordination.
- `src/documents.py`: evidence loading and chunking.
- `src/retrieval.py`: TF-IDF ranking.
- `src/assistant.py`: extractive/API response generation and basic guardrails.
- `src/audit.py`: local evidence log.
- `data/`: synthetic documents and metrics.
- `sql/evidence_log.sql`: evidence-log schema.
- `tests/test_controls.py`: automated control tests.
- `docs/`: architecture, control mapping and images.

## Tests

```bash
python -m pytest
```

See the test file for actual coverage. The presence of tests is not a claim that a particular revision has passed.

## Limitations

- Retrieval is lexical; embeddings and a vector database are not implemented.
- Citation checking tests label presence, not claim-level entailment or completeness.
- A weak-evidence refusal does not catch every unsupported question.
- SQLite logging is demonstrative; hosted storage can reset and is not an immutable audit record.
- The interface exposes the interaction log without per-user access controls. Use synthetic questions and data only.
- API mode sends the question and retrieved passages to the configured model provider.
- This prototype does not establish regulatory compliance or replace professional judgement.

## Planned improvements

Versioned evaluation datasets, claim-support checks, source-version controls, retrieval comparisons, authentication and durable evidence storage.

[Architecture](docs/architecture.md) · [Control mapping](docs/control_mapping.md) · [LinkedIn](https://www.linkedin.com/in/ernestowendling)
