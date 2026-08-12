# Étude de cas - Fiabilité et observabilité d'un pipeline d'inférence LLM asynchrone

Fiabilisation et instrumentation complète d'un pipeline d'inférence LLM asynchrone, validées par des campagnes de chaos engineering, pour une grande administration financière française.

## Context

**Role**: Ingénieur MLOps / Plateforme d'inférence LLM
**Client**: Une grande administration financière française (mission réalisée en sous-traitance)
**Période**: Depuis juin 2026

Les requêtes d'inférence devaient être traitées de manière asynchrone et résiliente, avec une visibilité de bout en bout sur leur cheminement, de la réception de la requête jusqu'à la réponse du modèle, sans perte en cas d'incident sur un composant de la chaîne.

## Technical approach

- **Traitement asynchrone**: workers `FastAPI` / `aiohttp` pour découpler la réception des requêtes de l'exécution de l'inférence, elle-même bornée par la disponibilité GPU.
- **File de messages**: `RabbitMQ` comme colonne vertébrale de distribution des tâches, gestion des retries et du backpressure entre la couche API et les workers d'inférence.
- **Tracing distribué**: instrumentation `OpenTelemetry` avec propagation du contexte `W3C TraceContext` à travers l'API, la file de messages et les workers d'inférence, permettant de suivre une requête de bout en bout à travers les frontières asynchrones.
- **Stack d'observabilité**: `Grafana` pour les dashboards, `Loki` pour l'agrégation centralisée des logs, `Tempo` pour le stockage et la visualisation des traces, corrélés via l'identifiant de trace.
- **Chaos engineering**: injection de pannes contrôlées (arrêt de worker, saturation de la file, éviction de pod GPU) pour valider la logique de retry/backoff et mesurer le comportement réel de récupération.

## My role

Conception de l'architecture asynchrone, instrumentation OpenTelemetry de bout en bout, construction des dashboards Grafana/Loki/Tempo, conduite des expériences de chaos engineering et fiabilisation du pipeline à partir des résultats observés.

## System diagram

```mermaid
flowchart LR
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Client]:::data --> B[FastAPI / aiohttp]:::compute
  B --> C[RabbitMQ]:::deploy
  C --> D[Workers d'inférence - vLLM]:::compute
  D --> E[Réponse / callback client]:::data
  B -.spans OTEL.-> F[Tempo]:::monitor
  C -.spans OTEL.-> F
  D -.spans OTEL.-> F
  B -.logs.-> G[Loki]:::monitor
  D -.logs.-> G
  F --> H[Grafana]:::monitor
  G --> H
```

## Chaos engineering

```mermaid
flowchart TB
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Injection de panne: worker kill, saturation file, éviction pod GPU]:::compute --> B[Observation via traces/logs/métriques]:::monitor
  B --> C[Mesure du comportement de retry/backoff]:::compute
  C --> D[Ajustement de la configuration de résilience]:::compute
  D --> A
```

## Results

- **Taux de succès des requêtes d'inférence**: [X]% en charge nominale, [Y]% en conditions de chaos engineering.
- **Temps de détection d'incident**: réduit à [N] minutes grâce à la corrélation traces/logs/métriques.
- **Temps de récupération (MTTR)** après incident simulé: [M] minutes.
- Couverture de traçabilité de bout en bout sur [Z]% des requêtes asynchrones.
