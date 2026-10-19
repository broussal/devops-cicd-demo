# devops-cicd-demo

Projet d'apprentissage de bout en bout : une petite API conteneurisée avec Docker, testée par un pipeline GitLab CI et déployée sur Kubernetes.

L'application est volontairement simple — un compteur de visites — pour se concentrer sur la chaîne de livraison plutôt que sur le code.

## Architecture

```
            ┌──────────── Kubernetes (kind) ─────────────────────────────────┐
requête ──> │ Service "api" ──> 3 Pods API ──> Service "redis" ──> Pod Redis │
            └────────────────────────────────────────────────────────────────┘
```

- **API** : Flask, servie par gunicorn. `/` incrémente le compteur, `/health` sert aux sondes.
- **Redis** : stocke le compteur, partagé par toutes les copies de l'API.

## Stack

Python · Flask · Redis · Docker · Docker Compose · GitLab CI · Kubernetes (kind)

## Structure

```
.
├── app/main.py        # l'API
├── requirements.txt   # dépendances Python
├── Dockerfile         # construction de l'image
├── compose.yaml       # lancement local avec Docker Compose
├── .gitlab-ci.yml     # pipeline CI
└── k8s/
    ├── api.yaml       # Deployment (3 réplicas, sondes) + Service de l'API
    └── redis.yaml     # Deployment + Service Redis
```

## Lancer en local avec Docker Compose

```bash
docker compose up -d --build
curl localhost:8000/
docker compose down
```

## Pipeline GitLab CI

À chaque `push` :

1. **build** — construit l'image (Docker-in-Docker) et la pousse dans le registre GitLab, taguée avec le hash du commit ;
2. **test** — récupère cette image, la lance avec Redis sur un réseau dédié et vérifie que l'API répond (`curl -f`).

L'image testée est exactement celle qui serait déployée : elle n'est construite qu'une fois.

## Déployer sur Kubernetes (kind)

```bash
kind create cluster --name demo
docker build -t compteur-api:v1 .
kind load docker-image compteur-api:v1 --name demo
kubectl apply -f k8s/
kubectl port-forward service/api 8000:8000
```

## Ce que le projet met en œuvre

- Conteneurisation d'une application et de ses dépendances
- Orchestration locale avec Docker Compose (réseau, DNS par nom de service, volume)
- Pipeline CI : build, publication dans un registre, test automatisé
- Versionnement des images par commit
- Déploiement Kubernetes déclaratif : Deployment, Service, réplicas
- Haute disponibilité : répartition de charge et recréation automatique des Pods
- Sondes de readiness et de liveness
- Infrastructure as code : tous les manifestes sont versionnés

## Pistes d'évolution

- Mise à jour progressive (rolling update) et retour arrière
- Scans de sécurité dans le pipeline
- Persistance des données Redis dans Kubernetes
- Déploiement automatique depuis le pipeline
