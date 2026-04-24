---
name: contribute
description: "Guider un contributeur a travers le workflow complet de contribution au repo : fork, clone, selection d'issue, branche, implementation, commit conventionnel et creation de PR. Utiliser quand un contributeur veut travailler sur une issue ou soumettre des changements."
allowed-tools: Read Bash Write Edit Glob Grep
---

Tu es un assistant specialise dans le workflow de contribution au repo **coding-dojo-ia-x-data**.

## Etape 1 — Verification des prerequis

Verifie que les outils necessaires sont installes :
```bash
gh auth status
uv --version
git --version
docker --version
```

Si `gh` n'est pas authentifie, guide l'utilisateur avec `gh auth login --web`.

## Etape 2 — Fork et clone

1. Verifie si un fork existe deja :
   ```bash
   gh repo list --json name | grep coding-dojo-ia-x-data
   ```

2. Si non, forke le repo :
   ```bash
   gh repo fork CAprogs/coding-dojo-ia-x-data --clone=false
   ```

3. Verifie si le repo est deja clone localement. Si non :
   ```bash
   gh repo clone <user>/coding-dojo-ia-x-data
   ```

4. Assure-toi que le remote `upstream` pointe vers `CAprogs/coding-dojo-ia-x-data` :
   ```bash
   git remote -v
   ```
   Si absent, l'ajouter :
   ```bash
   git remote add upstream https://github.com/CAprogs/coding-dojo-ia-x-data.git
   ```

## Etape 3 — Selection et assignation de l'issue

1. Si aucun numero d'issue n'est fourni, liste les issues ouvertes :
   ```bash
   gh issue list --repo CAprogs/coding-dojo-ia-x-data --limit 20
   ```
   Demande a l'utilisateur laquelle traiter.

2. Recupere les details de l'issue :
   ```bash
   gh issue view <issue-number> --repo CAprogs/coding-dojo-ia-x-data
   ```

3. Affiche un resume : titre, labels, description, criteres d'acceptation, dependances.

4. Demande confirmation avant de continuer.

5. S'assigne l'issue (ou laisse un commentaire si pas les droits) :
   ```bash
   gh issue edit <issue-number> --repo CAprogs/coding-dojo-ia-x-data --add-assignee @me
   ```

## Etape 4 — Creation de la branche de travail

1. Determine la branche cible en fonction des labels de l'issue. Par defaut : `lille`.

2. Synchronise et cree la branche :
   ```bash
   git fetch upstream
   git checkout -b feat/<issue-number>-<slug-court> upstream/<branche-cible>
   ```

   Convention de nommage : `feat/<issue-number>-<description-courte>` (ex: `feat/8-env-example`)

## Etape 5 — Implementation

1. Lis le `CLAUDE.md` pour comprendre l'architecture et les conventions.

2. Lis les fichiers pertinents avant de modifier quoi que ce soit.

3. Implemente les changements en respectant :
   - Les criteres d'acceptation de l'issue
   - Les conventions de code (Ruff, mypy, SQLFluff)
   - La structure du projet (`src/ingestion/`, `src/transformation/`, `src/exposition/`, `src/logger/`)

4. Verifie la qualite :
   ```bash
   uv run just quality-all
   ```

## Etape 6 — Commit et push

1. Utilise des commits conventionnels (commitizen configure) :
   - `feat:` nouvelle fonctionnalite
   - `fix:` correctif
   - `docs:` documentation
   - `refactor:` refactoring
   - `chore:` maintenance

2. Pousse la branche :
   ```bash
   git push -u origin feat/<issue-number>-<slug-court>
   ```

## Etape 7 — Creation de la Pull Request

1. Cree la PR ciblant la branche upstream :
   ```bash
   gh pr create \
     --repo CAprogs/coding-dojo-ia-x-data \
     --base <branche-cible> \
     --title "<type>: <description courte>" \
     --body "## Summary
   <description>

   Closes #<issue-number>

   ## Test plan
   - [ ] <checks>

   🤖 Generated with Claude Code"
   ```

2. Affiche l'URL de la PR.

3. Verifie la CI :
   ```bash
   gh pr checks <pr-number> --repo CAprogs/coding-dojo-ia-x-data --watch
   ```

## Regles

- Toujours lire les fichiers avant de les modifier
- Ne jamais push sur `main` ou les branches de mission directement
- Respecter les conventional commits
- Lancer `uv run just quality-all` avant de creer la PR
- Demander confirmation a l'utilisateur avant chaque action publique (commentaire, PR, push)
