# Project Context Memory

A local-first memory layer for research and coding agents. Save project decisions, dataset paths, experiment results, and open questions, then retrieve relevant context before an agent answers.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The SQLite database is created at `data/memory.db`.

## CLI examples

```bash
python memory_cli.py list
python memory_cli.py search "chunk size" --project research-rag
python memory_cli.py add --project research-rag --type decision --title "Use hybrid retrieval" --content "Evaluate dense retrieval plus BM25 before changing defaults."
python memory_cli.py export --project research-rag
```

## Inject memory into an agent

```python
from memory_store import MemoryStore

store = MemoryStore("data/memory.db")
context = store.build_context(
    project="research-rag",
    query="Which chunk size did we decide to test?",
    limit=5,
)
prompt = f"""Use this saved project context when answering.
If it does not contain the answer, say what is missing.

{context}

User question: Which chunk size did we decide to test?
"""
```

Keep project memory separate from retrieved research-paper passages. Memory records decisions and work history; RAG retrieval supplies source evidence.

## Memory types

- `decision`: durable choices and rationale
- `dataset`: paths, versions, access notes, caveats
- `experiment`: setup, metrics, results, interpretation
- `question`: unresolved questions or blockers
- `note`: other useful project context

## Privacy and limitations

- Data stays local in SQLite by default.
- Never store API keys, passwords, or private tokens.
- Dataset paths are stored as text; the app does not upload or inspect those files.
- `PROJECT_MEMORY.md` is generated for repository-friendly sharing. Review it before committing.
- Search currently uses keyword overlap, not embeddings.
- Memories are added explicitly; automatic extraction and LLM integration are future extensions.
- No authentication: intended for local development.
