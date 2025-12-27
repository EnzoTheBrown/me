# Case Study - OCR + Document Parsing Pipeline (Tantar)

Production OCR and parsing pipeline on Kubernetes, orchestrated by RabbitMQ, with S3 and Postgres storage. The flow includes Docling, docling-hierarchical-pdf, and an LLM layer for classification/extraction, plus a RAG dimension to link documents and build a timeline.

## Context

**Role**: Co-founder and Lead Product/Tech, Tantar  
**Period**: 2023 - present  

Goal: extract key legal information from documents (PDF), structure events, and deliver a reliable timeline for legal teams.

## Technical approach

- **Async pipeline**: decoupled workers, autoscaled by queue length (KEDA).
- **Robust parsing**: per-page OCR, logical reconstruction, and LLM classification by document type.
- **Structured extraction**: LLM extraction guided by schemas per document type.
- **RAG and timeline**: semantic indexing to link documents, then generation of a structured timeline.
- **Reliability**: idempotency, bounded retries, DLQ, statuses persisted in the DB.

## My role

Designed the architecture, defined the pipeline, integrated OCR/structure/classification/extraction workers, and oversaw extraction quality and timeline delivery.

## Pipeline diagram (OCR + Parsing)

```mermaid
flowchart LR
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Client]:::data --> B[API]:::deploy
  B -->|upload raw PDF| C[S3 / MinIO]:::data
  B -->|create doc + artifacts| D[Postgres]:::data
  B -->|publish doc.split| E[RabbitMQ ocr.jobs]:::compute

  E --> Q1[q_doc_split]:::compute
  Q1 --> F[Splitter]:::compute
  F -->|page PNGs| C
  F -->|pages + artifacts| D
  F -->|publish page.ocr| E

  E --> Q2[q_page_ocr]:::compute
  Q2 --> G[OCR]:::compute
  G -->|ocr JSON| C
  G -->|page status| D
  G -->|publish doc.structure| E

  E --> Q3[q_doc_structure]:::compute
  Q3 --> H[Structure]:::compute
  H -->|doc.json/doc.md| C
  H -->|doc status| D
  H -->|publish doc.classify| E

  E --> Q4[q_doc_classify]:::compute
  Q4 --> I[LLM classifier]:::compute
  I -->|classification.json| C
  I -->|doc status| D
  I -->|publish doc.extract| E

  E --> Q5[q_doc_extract]:::compute
  Q5 --> J[LLM extractor]:::compute
  J -->|extraction.json| C
  J -->|doc status| D
  J -->|publish doc.index| E

  E --> Q6[q_doc_index]:::compute
  Q6 --> K[Indexing]:::compute
  K -->|doc status DONE| D
```

## RAG + timeline diagram

```mermaid
flowchart TB
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e

  A[Structured extracts]:::data --> B[Semantic indexing]:::compute
  B --> C[Linked document search]:::compute
  C --> D[Event consolidation]:::compute
  D --> E[Timeline]:::deploy
  E --> F[Product UI]:::deploy
```

## Technical stack

- **API**: FastAPI, Python.
- **Pipeline**: RabbitMQ, KEDA, Kubernetes.
- **OCR and parsing**: Tesseract, Docling, docling-hierarchical-pdf.
- **Storage**: S3 / MinIO, Postgres.
- **LLM**: classification and extraction.
- **RAG**: semantic indexing and document linking.

## Results

- Stable, scalable, and traceable pipeline for sensitive legal documents.
- Full chain from raw PDF to an actionable timeline.
- Reduced reading and synthesis time for legal teams.
