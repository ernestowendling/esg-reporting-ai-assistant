# Control mapping

| Control objective | Prototype control | Evidence produced | Current limitation |
|---|---|---|---|
| Prevent unsupported claims | Minimum retrieval-score threshold and explicit refusal | Refusal status and top score in SQLite log | Threshold needs formal evaluation |
| Ensure source traceability | Source, section/row and chunk ID attached to every passage | Exact citation labels in answer and log | Synthetic documents do not yet have PDF page coordinates |
| Detect uncited model output | Post-generation citation validation | Invalid answer is replaced by control refusal | Validator checks citation presence, not claim-level completeness |
| Preserve human accountability | Mandatory human-review label | Human-review flag in every log row | No authenticated approval workflow yet |
| Reconstruct each interaction | SQLite evidence log | Question, answer, model, sources, scores and timestamp | Community Cloud filesystem is not durable |
| Protect confidential information | Synthetic data only; secrets excluded from Git | Data disclaimer, `.gitignore`, `.env.example` | Production data classification is out of scope |
