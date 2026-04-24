---
name: contribute
description: Guide the full contributing workflow for this coding dojo project — setup, branch creation, code quality checks, conventional commits, and PR creation. Use when the user wants to contribute to the project, create a new branch, run quality checks, commit changes, or open a pull request.
argument-hint: [setup|branch|quality|commit|pr]
allowed-tools: [Bash, Read, Edit, Write]
---

# Contribute

Gère l'intégralité du workflow contributing pour ce coding dojo (Paris Events Analyzer).

## Contexte projet

- **Stack** : Python 3.12, uv, just, MinIO, DuckDB, dbt-core, Streamlit, pre-commit, commitizen, Ruff, mypy, SQLFluff
- **Branches missions** : `mission-1-uv`, `mission-2-pre-commit`, `mission-3-commitizen`, `mission-4-ruff-mypy`, `mission-5-sqlfluff`
- **Branche cible PR** : `lille`
- **Branche de référence** : `main`

## Arguments optionnels

Si `$ARGUMENTS` est précisé, sauter directement à l'étape correspondante :
- `setup` → Étape 1 seulement
- `branch` → Étape 2 seulement
- `quality` → Étape 3 seulement
- `commit` → Étape 4 seulement
- `pr` → Étapes 3 + 5 (qualité complète + PR)

Sans argument : analyser l'état courant et exécuter les étapes pertinentes.

## Workflow

### 1. Setup de l'environnement

Vérifier si `.venv/` existe et si `uv.lock` est synchronisé. Si non :

```bash
uv sync --frozen --all-groups
uv pip install -e .
```

Vérifier si pre-commit est installé (`.git/hooks/pre-commit`). Si non :

```bash
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

Expliquer à quoi sert chaque commande (c'est un dojo d'apprentissage).

### 2. Gestion de la branche

- Si on est sur `main` ou `lille` : demander sur quelle mission le contributeur travaille (1 à 5), puis créer une branche depuis la bonne branche mission :
  ```bash
  git checkout mission-<N>-<nom>
  git checkout -b feat/<description-courte>
  ```
- Si on est déjà sur une branche de travail : vérifier qu'elle est basée sur la bonne branche mission (pas `main`).
- Signaler si la branche locale est en retard sur son remote.

### 3. Vérifications qualité (fichiers modifiés)

```bash
uv run just quality-default
```

En cas d'échec, diagnostiquer et corriger :
- **Ruff** : `uv run ruff check --fix . && uv run ruff format .`
- **mypy** : afficher les erreurs de types et proposer les corrections
- **SQLFluff** : `uv run sqlfluff fix --dialect duckdb .`
- **trailing-whitespace / end-of-file** : les hooks corrigent automatiquement, relancer `git add`

Conventions à rappeler si violation :
- Python : 120 chars max par ligne, docstrings Google style
- SQL : keywords UPPERCASE, identifiers lowercase, 230 chars max/ligne

### 4. Commit conventionnel

Format : `<type>(<scope>): <description>`

**Types valides** : `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`, `style`

**Scopes courants** : `ingestion`, `transformation`, `exposition`, `ci`, `docs`, `hooks`, `deps`

Si commitizen est disponible (mission-3+) :
```bash
uv run cz commit
```

Sinon, guider vers le bon message et committer :
```bash
git commit -m "<type>(<scope>): <description>"
```

Ne jamais utiliser `--no-verify`.

### 5. Création de la Pull Request

Avant d'ouvrir la PR, lancer la qualité sur tous les fichiers :
```bash
uv run just quality-all
```

Vérifier qu'aucun fichier sensible n'est inclus (`.env`, credentials).

La PR cible **toujours** la branche `lille`. Créer avec le template du projet :

```bash
git push -u origin <branche-courante>
gh pr create --base lille \
  --title "<type>(<scope>): <description>" \
  --body "$(cat .github/PULL_REQUEST_TEMPLATE/pull_request_template.md)"
```

Si le template n'existe pas encore (missions 1-2), utiliser ce body :

```
Merci pour ta contribution au sein de PARIS-EVENTS-ANALYZER ᕙ(⇀‸↼‶)ᕗ

- [x] Tu as respecté l'architecture du livrable 🎯
- [x] Tu n'as pas inclus de fichiers sensibles ⚠️
- [x] Tu as compris l'utilité des outils mis en avant dans cette mission 💡
```

## Comportement

- Toujours expliquer le **pourquoi** de chaque étape (contexte pédagogique).
- Si une étape échoue : diagnostiquer la cause avant de continuer.
- Confirmer avec le contributeur avant toute modification de code.
- Ne jamais skipper les hooks (`--no-verify` est interdit).
