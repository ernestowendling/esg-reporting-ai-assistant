# Architecture

```mermaid
flowchart LR
    U[User] --> UI[Streamlit interface]
    UI --> R[TF-IDF evidence retriever]
    D[Synthetic ESG documents and metrics] --> R
    R --> G{Evidence score above threshold?}
    G -- No --> X[Controlled refusal]
    G -- Yes --> C[Claude grounded drafting or extractive demo]
    C --> V[Citation validation]
    V --> A[Draft answer plus citations]
    X --> L[(SQLite evidence log)]
    A --> L
    A --> H[Human review required]
```

## Production evolution

1. Replace TF-IDF with embeddings and a managed vector store.
2. Parse controlled source PDFs with page-level metadata.
3. Persist the evidence log in PostgreSQL with authenticated users.
4. Add evaluation datasets for retrieval quality, faithfulness and refusal behaviour.
5. Integrate governed ESG metrics from source systems, including an SAP-oriented interface layer.
