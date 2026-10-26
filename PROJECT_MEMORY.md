# Project Memory: research-rag

> Starter template — illustrative examples only. Replace with verified project facts.

## Decisions

### Separate project memory from document retrieval
Store durable project decisions and experiment history separately from evidence retrieved from research papers. Include them as distinct prompt sections.

## Datasets

### Dataset layout
- Raw files: `data/raw/`
- Processed chunks and metadata: `data/processed/`
- Do not commit private datasets, secrets, or generated indexes.

## Experiments

### Retrieval baseline
Status: NOT RUN. Record Recall@5, MRR@10, answer faithfulness, and latency after executing the evaluation.

## Questions

### Chunking strategy
Compare fixed-size chunks with section-aware chunking. Record chunk size, overlap, embedding model, top-k, Recall@5, and latency.
