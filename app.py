"""Streamlit entry point for the ESG Reporting AI Assistant prototype."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

from src.assistant import answer_question
from src.audit import log_interaction, read_log
from src.documents import load_evidence
from src.retrieval import EvidenceRetriever

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = BASE_DIR / "evidence_log.db"

st.set_page_config(
    page_title="ESG Reporting AI Assistant",
    page_icon="📊",
    layout="wide",
)


@st.cache_resource
def build_retriever() -> EvidenceRetriever:
    return EvidenceRetriever(load_evidence(DATA_DIR))


def get_secret(name: str) -> str | None:
    """Read a value from Streamlit secrets first, then environment variables."""
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except FileNotFoundError:
        pass
    return os.getenv(name)


retriever = build_retriever()

st.title("ESG Reporting AI Assistant")
st.caption("Public prototype · synthetic data only · every answer requires human review")

with st.sidebar:
    st.header("Control settings")
    top_k = st.slider("Evidence chunks retrieved", 2, 6, 4)
    minimum_score = st.slider(
        "Minimum retrieval score",
        min_value=0.05,
        max_value=0.50,
        value=0.20,
        step=0.01,
        help="Below this threshold, the assistant refuses to answer.",
    )
    api_key_present = bool(get_secret("ANTHROPIC_API_KEY"))
    st.metric("Claude API", "Connected" if api_key_present else "Demo mode")
    st.info(
        "Control signature: source citation, no-evidence refusal, evidence log, "
        "and mandatory human review."
    )

qa_tab, evidence_tab, audit_tab, about_tab = st.tabs(
    ["Ask a question", "Retrieved evidence", "Audit log", "About the controls"]
)

with qa_tab:
    examples = [
        "What was the fund's financed-emissions intensity in 2025?",
        "What engagement escalation is required after two unsuccessful cycles?",
        "Which principal adverse impact indicator exceeded its threshold?",
        "What was the fund's water consumption in 2025?",
    ]
    selected_example = st.selectbox("Example question", [""] + examples)
    question = st.text_area(
        "ESG reporting question",
        value=selected_example,
        height=100,
        placeholder="Ask a question that should be answered only from the synthetic evidence library.",
    )

    if st.button("Retrieve evidence and draft answer", type="primary"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            results = retriever.retrieve(question, top_k=top_k)
            answer, model, human_review_required = answer_question(
                question=question,
                results=results,
                minimum_score=minimum_score,
                api_key=get_secret("ANTHROPIC_API_KEY"),
                model=get_secret("ANTHROPIC_MODEL"),
            )
            log_interaction(
                database_path=DATABASE_PATH,
                question=question,
                answer=answer,
                model=model,
                results=results,
                human_review_required=human_review_required,
            )
            st.session_state["last_results"] = results
            st.session_state["last_answer"] = answer
            st.session_state["last_model"] = model

    if "last_answer" in st.session_state:
        if st.session_state["last_answer"].startswith("INSUFFICIENT EVIDENCE:"):
            st.error(st.session_state["last_answer"])
        else:
            st.markdown(st.session_state["last_answer"])
        st.warning("Human review required before any reporting or disclosure use.")
        st.caption(f"Generation mode: {st.session_state['last_model']}")

with evidence_tab:
    results = st.session_state.get("last_results", [])
    if not results:
        st.info("Run a question to inspect the retrieved evidence.")
    for rank, result in enumerate(results, start=1):
        with st.expander(
            f"#{rank} · score {result.score:.3f} · {result.chunk.citation}",
            expanded=rank == 1,
        ):
            st.write(result.chunk.text)

with audit_tab:
    st.subheader("Evidence and decision log")
    st.caption(
        "The public MVP uses local SQLite. On Community Cloud this log is demonstrative, "
        "not durable storage, and can reset when the app restarts."
    )
    log_frame = read_log(DATABASE_PATH)
    if log_frame.empty:
        st.info("No interactions logged yet.")
    else:
        st.dataframe(log_frame, use_container_width=True, hide_index=True)
        st.download_button(
            "Download audit log as CSV",
            data=log_frame.to_csv(index=False).encode("utf-8"),
            file_name="esg_assistant_audit_log.csv",
            mime="text/csv",
        )

with about_tab:
    st.markdown(
        """
### What this prototype demonstrates

- **Grounding:** the assistant receives only retrieved source passages.
- **Traceability:** retrieved chunks retain source and location metadata.
- **No evidence → no answer:** weak retrieval triggers an explicit refusal.
- **Citation validation:** an LLM answer is rejected if it does not contain a supplied citation.
- **Human in the loop:** every output is a draft and requires review.
- **Audit trail:** the question, evidence, model, result and status are logged.

### Honest MVP boundary

This first public version uses transparent TF-IDF retrieval rather than embeddings and a vector database. The next technical increment is to replace the retriever with an embedding-based store while preserving the same citation and audit controls.
        """
    )
