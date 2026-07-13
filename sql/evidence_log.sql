-- Evidence log used by the public prototype.
-- The table records what the user asked, which evidence was retrieved,
-- whether the assistant answered or refused, and whether human review is required.

CREATE TABLE IF NOT EXISTS evidence_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc TEXT NOT NULL,
    question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('answered', 'refused')),
    model TEXT NOT NULL,
    top_retrieval_score REAL NOT NULL,
    sources_json TEXT NOT NULL,
    answer TEXT NOT NULL,
    human_review_required INTEGER NOT NULL CHECK (human_review_required IN (0, 1))
);

-- Auditor-oriented review query: show refusals and weak retrievals first.
SELECT
    id,
    timestamp_utc,
    question,
    status,
    model,
    ROUND(top_retrieval_score, 3) AS top_retrieval_score,
    human_review_required
FROM evidence_log
ORDER BY
    CASE WHEN status = 'refused' THEN 0 ELSE 1 END,
    top_retrieval_score ASC,
    timestamp_utc DESC;
