---
name: check-contribution
description: >
  Lance une revue complète pré-contribution selon les bonnes pratiques GitHub et les conventions
  du dépôt. Déclencher quand l'utilisateur demande à vérifier, relire ou valider sa contribution,
  ses commits ou sa branche avant d'ouvrir une pull request. Également sur les formulations
  "je suis prêt à faire une PR ?", "vérifie mon travail", "valide mes changements", "revue avant merge".
---

# check-contribution

Tu joues le rôle d'un ingénieur senior effectuant une revue pré-contribution. Exécute les vérifications suivantes dans l'ordre et produis un rapport structuré PASS/FAIL à la fin. Corrige les problèmes automatiquement quand c'est possible ; demande confirmation avant toute action destructive.

---

## 1. Nommage de la branche

Commande : `git rev-parse --abbrev-ref HEAD`

Le nom de branche doit commencer par l'un de ces préfixes : `feature/`, `fix/`, `bugfix/`, `hotfix/`, `chore/`, `docs/`, `refactor/`, `test/`, `ci/`, `perf/`.

- PASS : la branche respecte la convention.
- FAIL : indiquer le nom de branche et le pattern attendu. Ne PAS renommer la branche automatiquement — demander à l'utilisateur.

---

## 2. Messages de commit

Commande : `git log origin/lille..HEAD --format="%H %s"` (ou `origin/main..HEAD` si sur main).

Chaque sujet de commit doit suivre les **Conventional Commits** (imposé par commitizen dans ce dépôt) :

```
<type>[scope optionnel]: <description>
```

Types valides : `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Règles :
- Sujet ≤ 72 caractères.
- Mode impératif, sans point final.
- Pas de commits avec `WIP`, `tmp`, `TODO`, `fixup!`, `squash!` dans le sujet (ils doivent être squashés avant le merge).

Pour chaque commit non conforme, afficher le hash + sujet et la règle violée. Proposer de reformuler interactivement avec `git rebase -i`.

---

## 3. Changements stagés / non stagés

Commandes : `git status --short` et `git diff --stat`.

- FAIL s'il y a des changements non commités appartenant à la feature (rappeler à l'utilisateur de commiter ou stasher).
- WARN s'il y a des fichiers non trackés qui ressemblent à du code source (`.py`, `.sql`, `.yml`, `.toml`, `.md`).

---

## 4. Qualité du code — Python

Commande : `just lint` (qui exécute ruff check + ruff format --check + mypy).

Si `just` n'est pas disponible, utiliser :
```
uv run ruff check src/
uv run ruff format --check src/
uv run mypy src/
```

- PASS : zéro erreur/avertissement.
- FAIL : afficher la sortie de l'outil telle quelle, puis proposer la correction automatique avec `just format` (ruff) ou afficher les erreurs mypy pour résolution manuelle.

---

## 5. Qualité du code — SQL

Commande : `just dbt-lint` ou `uv run sqlfluff lint src/transformation/dbt_paris_event_analyzer/ --dialect duckdb`.

- PASS : zéro violation.
- FAIL : afficher les violations. Proposer la correction automatique avec `just dbt-lint-fix`.

---

## 6. Hooks pre-commit

Commande : `uv run pre-commit run --all-files`.

Valide les espaces en fin de ligne, EOF, syntaxe YAML/TOML, format des commits conventionnels (le hook commit-msg n'est déclenché qu'au commit — l'ignorer ici), ruff, mypy et sqlfluff.

- PASS : tous les hooks sont verts.
- FAIL : afficher la sortie des hooks et proposer de laisser pre-commit corriger ce qu'il peut (`pre-commit run --all-files` une seconde fois après les hooks auto-correctifs).

---

## 7. Nombre d'appels logger

Commande : `grep -rn "logger\." src/ --include="*.py" | wc -l`

Le projet impose **exactement 12 appels logger** dans tous les fichiers Python source (contrainte CI documentée dans CLAUDE.md).

- PASS : comptage == 12.
- FAIL : indiquer le comptage réel et lister les fichiers concernés.

---

## 8. Checklist PR

Inspecter le diff par rapport à la branche de base (`git diff origin/lille...HEAD --stat`).

Vérifier et reporter chaque point :

| Élément | Vérification |
|---------|--------------|
| Commits significatifs | Au moins 1 commit au-delà de la base |
| Pas d'artefacts de debug | Aucun `print()`, `breakpoint()`, `pdb`, `ipdb`, `import pdb` dans les fichiers `.py` |
| Pas de secrets | Aucun mot de passe, token ou clé API en dur (patterns : `password\s*=\s*["']`, `token\s*=\s*["']`, `api_key\s*=\s*["']`) |
| Docs à jour | Si `src/` a changé, vérifier si `README.md` ou `CLAUDE.md` nécessitent une mise à jour — signaler sans modifier |
| `.env` non commité | `.env` ne doit pas apparaître dans `git diff --name-only origin/lille...HEAD` |
| Version `pyproject.toml` | S'il s'agit d'un commit de release, rappeler de bumper la version avec `cz bump` |

---

## 9. Rapport de synthèse

Après toutes les vérifications, afficher un tableau de synthèse :

```
┌─────────────────────────────────┬────────┐
│ Vérification                    │ Statut │
├─────────────────────────────────┼────────┤
│ Nommage de branche              │ PASS   │
│ Messages de commit              │ PASS   │
│ Changements non commités        │ PASS   │
│ Lint Python (ruff + mypy)       │ FAIL   │
│ Lint SQL (sqlfluff)             │ PASS   │
│ Hooks pre-commit                │ FAIL   │
│ Comptage appels logger          │ PASS   │
│ Checklist PR                    │ PASS   │
└─────────────────────────────────┴────────┘

Problèmes à corriger avant d'ouvrir une PR :
  [1] ruff: E501 ligne trop longue — src/ingestion/fetch.py:42
  [2] pre-commit: espace en fin de ligne — src/transformation/dbt_paris_event_analyzer/models/silver/events.sql
```

Conclure par :
- "Prêt à ouvrir une PR." (tous les checks PASS)
- "Corrige les N problème(s) ci-dessus, puis relance /check-contribution." (au moins un FAIL)
