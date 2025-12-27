# Étude de cas - Plateforme d’automatisation des paiements (iBanFirst)

Plateforme distribuée d’analyse documentaire et de création automatique de paiements, conçue pour la fiabilité, la traçabilité et la scalabilité.

## Contexte

**Poste**: Lead Backend & GenAI, iBanFirst  
**Période**: 2024 - présent  

Objectif: automatiser l’extraction des données de factures et la création de paiements, tout en respectant des contraintes fortes de qualité, de conformité et de sécurité.

## Approche technique

- **Pipeline documentaire**: ingestion, extraction, normalisation et validation des champs critiques.
- **Orchestration**: architecture distribuée avec workers asynchrones pour traiter des volumes élevés.
- **API**: endpoints clairs pour déclencher l’analyse, récupérer les résultats et piloter la création des paiements.
- **Observabilité**: suivi de la latence, du taux d’erreur et des anomalies pour garantir la stabilité en prod.
- **Sécurité & conformité**: traçabilité complète des décisions et versions de modèles.

## Stack technique

- **Backend**: FastAPI, Pydantic, Python, asyncio.
- **Eventing**: Kafka.
- **Stockage**: AWS S3.
- **Infra**: Docker.
- **Observabilité**: Grafana, Prometheus, OpenTelemetry.

## Mon rôle

Conception de l’architecture distribuée, développement d’un worker capable de parser des milliers de documents, mise en place du module de création automatique des paiements, et supervision de la qualité globale en production.

## Schéma système (Ingestion + Extraction + Paiement)

```mermaid
flowchart LR
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Factures fournisseurs]:::data --> B[Ingestion + stockage]:::data
  B --> C[Workers d’extraction asynchrones]:::compute
  C --> D[Normalisation + validation]:::compute
  D --> E[API de décision paiement]:::deploy
  E --> F[Création de paiement]:::deploy
  D --> G[Journal d’audit]:::monitor
  E --> G
  F --> G
```

## Boucle de qualité

```mermaid
flowchart TB
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Retours métier + erreurs prod]:::data --> B[Analyse des causes]:::compute
  B --> C[Amélioration extraction + règles]:::compute
  C --> D[Tests de non-régression]:::compute
  D --> E[Déploiement contrôlé]:::monitor
  E --> A
```

## Résultats

- **Latence**: < 1 seconde par fichier.
- **Taux d’erreur**: < 1%.
- Réduction significative du temps de traitement des paiements.
- Diminution des erreurs humaines via une automatisation fiable.
- Stabilité renforcée grâce à une observabilité et une traçabilité end-to-end.

