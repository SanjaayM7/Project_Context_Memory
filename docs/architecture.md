# Architecture

```text
User / coding agent -> MemoryStore.build_context() -> SQLite keyword search
                                            |
                                            v
                              Retrieved memory context pack
                                            |
                         +------------------+------------------+
                         v                                     v
                 LLM prompt memory section           Research RAG passages
```

## Memory lifecycle
1. Capture durable facts after decisions, dataset changes, experiments, or blockers.
2. Store under a project key with type, tags, and source.
3. Retrieve a small number of relevant memories before the agent answers.
4. When a decision changes, mark the old record `superseded` and add the replacement.
5. Export and review `PROJECT_MEMORY.md` periodically.

## Evaluation
Compare a baseline agent without memory against a memory-aware agent. Track:
- Answerable-memory recall: correct saved fact appears in retrieved context.
- Repeated-question rate: agent asks for information already stored.
- Unsupported-answer rate: agent claims facts absent from memory.
- Retrieval latency.

Use labelled expected answers; plausible-sounding answers are not necessarily correct.
