# Case Study - Payment Automation Platform (iBanFirst)

Distributed document analysis and automatic payment creation platform, designed for reliability, traceability, and scalability.

## Context

**Role**: Lead Backend and GenAI, iBanFirst  
**Period**: 2024 - present  

Goal: automate invoice data extraction and payment creation while meeting strong requirements for quality, compliance, and security.

## Technical approach

- **Document pipeline**: ingestion, extraction, normalization, and validation of critical fields.
- **Orchestration**: distributed architecture with asynchronous workers to handle high volumes.
- **API**: clear endpoints to trigger analysis, retrieve results, and drive payment creation.
- **Observability**: latency, error rate, and anomaly tracking to ensure production stability.
- **Security and compliance**: full traceability of decisions and model versions.

## Technical stack

- **Backend**: FastAPI, Pydantic, Python, asyncio.
- **Eventing**: Kafka.
- **Storage**: AWS S3.
- **Infra**: Docker.
- **Observability**: Grafana, Prometheus, OpenTelemetry.

## My role

Designed the distributed architecture, built a worker capable of parsing thousands of documents, implemented the automatic payment creation module, and supervised overall production quality.

## System diagram (Ingestion + Extraction + Payment)

```mermaid
flowchart LR
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Supplier invoices]:::data --> B[Ingestion + storage]:::data
  B --> C[Async extraction workers]:::compute
  C --> D[Normalization + validation]:::compute
  D --> E[Payment decision API]:::deploy
  E --> F[Payment creation]:::deploy
  D --> G[Audit log]:::monitor
  E --> G
  F --> G
```

## Quality loop

```mermaid
flowchart TB
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Business feedback + prod errors]:::data --> B[Root cause analysis]:::compute
  B --> C[Extraction + rules improvements]:::compute
  C --> D[Non-regression tests]:::compute
  D --> E[Controlled deployment]:::monitor
  E --> A
```

## Results

- **Latency**: < 1 second per file.
- **Error rate**: < 1%.
- Significant reduction in payment processing time.
- Fewer human errors through reliable automation.
- Stronger stability thanks to end-to-end observability and traceability.
