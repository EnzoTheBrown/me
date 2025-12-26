# Étude de cas - Pipeline OCR + Parsing documentaire (Tantar)

Pipeline OCR et parsing en production sur Kubernetes, orchestré par RabbitMQ, avec stockage S3 et Postgres. Le flux intègre Docling, docling-hierarchical-pdf, et une couche LLM pour classification/extraction, plus une dimension RAG pour relier les pièces et construire une frise chronologique.

## Contexte

**Poste**: Cofondateur & Lead Produit / Tech, Tantar  
**Période**: 2023 - présent  

Objectif: extraire des informations juridiques clés depuis des documents (PDF), structurer les événements, et restituer une frise chronologique fiable pour les équipes juridiques.

## Approche technique

- **Pipeline asynchrone**: workers découplés, autoscalés par la longueur de file (KEDA).
- **Parsing robuste**: OCR par page, reconstruction logique, et classification LLM par type de document.
- **Extraction structurée**: extraction LLM guidée par schémas selon le type de pièce.
- **RAG et frise chronologique**: indexation sémantique pour relier les pièces, puis génération d’une timeline structurée.
- **Fiabilité**: idempotence, retries bornés, DLQ, statuts persistés en base.

## Mon rôle

Conception de l’architecture, définition du pipeline, intégration des workers OCR/structure/classification/extraction, supervision de la qualité d’extraction et de la restitution en frise chronologique.

## Schéma du pipeline (OCR + Parsing)

```mermaid
flowchart LR
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Client]:::data --> B[API]:::deploy
  B -->|upload PDF brut| C[S3 / MinIO]:::data
  B -->|creation doc + artefacts| D[Postgres]:::data
  B -->|publish doc.split| E[RabbitMQ ocr.jobs]:::compute

  E --> Q1[q_doc_split]:::compute
  Q1 --> F[Splitter]:::compute
  F -->|pages PNG| C
  F -->|pages + artefacts| D
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
  Q4 --> I[Classifier LLM]:::compute
  I -->|classification.json| C
  I -->|doc status| D
  I -->|publish doc.extract| E

  E --> Q5[q_doc_extract]:::compute
  Q5 --> J[Extractor LLM]:::compute
  J -->|extraction.json| C
  J -->|doc status| D
  J -->|publish doc.index| E

  E --> Q6[q_doc_index]:::compute
  Q6 --> K[Indexation]:::compute
  K -->|doc status DONE| D
```

## Schéma RAG + frise chronologique

```mermaid
flowchart TB
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e

  A[Extraits structurés]:::data --> B[Indexation sémantique]:::compute
  B --> C[Recherche de pièces liées]:::compute
  C --> D[Consolidation d’événements]:::compute
  D --> E[Frise chronologique]:::deploy
  E --> F[UI produit]:::deploy
```

## Stack technique

- **API**: FastAPI, Python.
- **Pipeline**: RabbitMQ, KEDA, Kubernetes.
- **OCR & parsing**: Tesseract, Docling, docling-hierarchical-pdf.
- **Stockage**: S3 / MinIO, Postgres.
- **LLM**: classification + extraction.
- **RAG**: indexation sémantique et rapprochement documentaire.

## Résultats

- Pipeline stable, scalable et traçable pour des documents juridiques sensibles.
- Chaîne complète du PDF brut jusqu’à la frise chronologique exploitable.
- Réduction du temps de lecture et de synthèse pour les équipes juridiques.
