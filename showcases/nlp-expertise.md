# Étude de cas - Fine-Tuning NLP pour le routage SAV (AWS SageMaker)

Système de classification robuste pour router des demandes SAV avec une priorité stricte à la precision et une boucle d’amélioration continue.

## Contexte

**Poste**: Data Scientist Junior, Like A Bird  
**Période**: 2018-2022  

J’ai conçu un système de classification de texte pour router les demandes SAV (service après-vente) vers le bon service. Le dataset comprenait 10 000+ requêtes réelles, annotées via une plateforme interne. Le déséquilibre des classes a été traité par augmentation de bruit et par des exemples synthétiques rédigés par des experts métier.

## Approche technique

- **Modèle**: `bert-base-uncased`, choisi pour ses performances de base solides et un fine-tuning efficace.
- **Entraînement**: SageMaker Training Jobs via une image Docker personnalisée pour garantir la reproductibilité.
- **Évaluation**: Accuracy, precision et recall, avec une préférence forte pour la precision afin d’éviter les routages hors sujet (philosophie Like A Bird: mieux vaut escalader à un humain que mal router).
- **Déploiement**: Batch Transform pour l’évaluation hors-prod et Endpoint managé pour l’inférence temps réel.
- **Monitoring**: Plateforme d’annotation exposant les prédictions, avec priorisation des outliers pour se concentrer sur les cas incertains.
- **Contraintes**: Exigences strictes de confidentialité, sans services SaaS externes.

## Mon rôle

Pilotage du développement modèle, des pipelines d’entraînement et d’inférence, de la logique d’évaluation, de l’intégration SageMaker, de la containerisation Docker et des services backend. Collaboration avec un ingénieur Vue.js pour l’interface d’annotation.

## Schéma système (Entraînement et inférence)

```mermaid
flowchart LR
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e
  classDef monitor fill:#f7eef4,stroke:#8a3a6f,stroke-width:1px,color:#2e0f22

  A[Requêtes SAV clients]:::data --> B[Plateforme d’annotation]:::data
  B --> C[Curated labeled dataset]:::data
  C --> D[Job d’entraînement SageMaker]:::compute
  D --> E[Artefact modèle]:::compute
  E --> F[Évaluation Batch Transform]:::compute
  E --> G[Endpoint temps réel]:::deploy
  F --> H[Dashboard d’évaluation]:::monitor
  G --> I[Service de routage en production]:::deploy
```

## Boucle d’amélioration

```mermaid
flowchart TB
  classDef data fill:#f7f4ed,stroke:#a8834a,stroke-width:1px,color:#2b1f10
  classDef compute fill:#eef7f0,stroke:#3f7f4c,stroke-width:1px,color:#102b1a
  classDef deploy fill:#eef2f7,stroke:#3a5f8a,stroke-width:1px,color:#0e1f2e

  A[Annotations: teach + check]:::data --> B[Job d’entraînement SageMaker]:::compute
  B --> C[Évaluation Batch Transform]:::compute
  C --> D[Mode observateur sur trafic prod]:::deploy
  D --> E[Comparaison manuelle vs baseline prod]:::compute
  E -- Insuffisant --> A
  E -- Suffisant --> F[Promotion vers l’endpoint prod]:::deploy
```

## Résultats

- **Qualité modèle**: Accuracy > 0.95, precision > 0.95, recall > 0.8.
- **Philosophie de routage**: priorité à la precision pour éviter les erreurs; en cas d’incertitude, escalade à un humain plutôt que mauvais routage.
- Itérations plus rapides sur les modèles de routage SAV grâce à une boucle d’amélioration automatisée.
- Déploiement contrôlé via un mode observateur avant promotion en temps réel.
- Effort d’annotation réduit dans le temps en ciblant les outliers et les prédictions incertaines.

Si tu veux, partage des métriques réelles (precision/recall, impact sur le routage) et je les intègre précisément.
