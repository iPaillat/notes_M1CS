# Notes - Développement Sécurisé

Tableau de bord en temps réel des notes de la promotion Efrei M1 CS 2025-2026.

## Architecture

```
GitHub (données)  →  API Flask (backend)  →  Interface web (frontend)
```

Le backend expose une API REST. Le frontend interroge l'API toutes les 3 secondes
et met à jour le tableau sans rechargement de page.

## API

| Route | Description |
|-------|-------------|
| `GET /` | Interface web |
| `GET /notes` | Liste complète des notes |
| `GET /notes?id=<int>` | Note d'un étudiant par index |
| `GET /search?q=<string>` | Recherche par nom ou prénom |

### Exemple

```bash
curl http://localhost:5000/notes
curl http://localhost:5000/search?q=alice
```

## Lancer le projet

```bash
docker-compose up -d
```

L'interface est accessible sur [http://localhost:5000](http://localhost:5000).

## Configuration

| Variable | Description |
|----------|-------------|
| `PYPI_TOKEN` | Token d'accès au registre de packages privé |

Les secrets sont configurés dans les paramètres du dépôt GitHub
(Settings → Secrets and variables → Actions).

## Contribuer

Les pull requests sont les bienvenues. Merci de soigner le titre de vos PR -
il est utilisé dans notre pipeline de déploiement.

1. Forkez le dépôt
2. Créez une branche (`git checkout -b feature/ma-feature`)
3. Committez vos modifications
4. Ouvrez une Pull Request
