Guide le contributeur à travers le workflow de contribution au repo coding-dojo-ia-x-data.

## Arguments
Format : `$ARGUMENTS` = `<issue-number>` (ex: `8`, `14`)

Si l'argument est manquant, lister les issues ouvertes et demander laquelle traiter.

---

## Etape 1 — Vérification des prérequis

Vérifier que les outils nécessaires sont installés :
```bash
gh auth status
uv --version
git --version
docker --version
```

Si `gh` n'est pas authentifié, guider l'utilisateur avec `gh auth login --web`.

---

## Etape 2 — Fork et clone

1. Vérifier si un fork existe déjà :
   ```bash
   gh repo list --json name | grep coding-dojo-ia-x-data
   ```

2. Si non, forker le repo :
   ```bash
   gh repo fork CAprogs/coding-dojo-ia-x-data --clone=false
   ```

3. Vérifier si le repo est déjà cloné localement. Si non :
   ```bash
   gh repo clone <user>/coding-dojo-ia-x-data
   ```

4. S'assurer que le remote `upstream` pointe vers `CAprogs/coding-dojo-ia-x-data` :
   ```bash
   git remote -v
   ```
   Si absent, l'ajouter :
   ```bash
   git remote add upstream https://github.com/CAprogs/coding-dojo-ia-x-data.git
   ```

---

## Etape 3 — Sélection et assignation de l'issue

1. Récupérer les détails de l'issue :
   ```bash
   gh issue view <issue-number> --repo CAprogs/coding-dojo-ia-x-data
   ```

2. Afficher un résumé de l'issue à l'utilisateur :
   - Titre
   - Labels (priorité, taille, domaine)
   - Description et critères d'acceptation
   - Dépendances éventuelles

3. Demander confirmation à l'utilisateur avant de continuer.

4. S'assigner l'issue (si on a les droits) :
   ```bash
   gh issue edit <issue-number> --repo CAprogs/coding-dojo-ia-x-data --add-assignee @me
   ```
   Si pas les droits, laisser un commentaire :
   ```bash
   gh issue comment <issue-number> --repo CAprogs/coding-dojo-ia-x-data --body "Je prends cette issue."
   ```

---

## Etape 4 — Création de la branche de travail

1. Déterminer la branche cible en fonction des labels de l'issue ou du contexte.
   Par défaut, partir de la branche `lille` (branche principale de contribution).

2. Synchroniser et créer la branche :
   ```bash
   git fetch upstream
   git checkout -b feat/<issue-number>-<slug-court> upstream/<branche-cible>
   ```

   Convention de nommage : `feat/<issue-number>-<description-courte>` (ex: `feat/8-env-example`)

---

## Etape 5 — Implémentation

1. Lire le `CLAUDE.md` pour comprendre l'architecture et les conventions du projet.

2. Lire les fichiers pertinents avant de modifier quoi que ce soit.

3. Implémenter les changements en respectant :
   - Les critères d'acceptation de l'issue
   - Les conventions de code (Ruff, mypy, SQLFluff configurés dans `pyproject.toml` et `.sqlfluff`)
   - La structure du projet (`src/ingestion/`, `src/transformation/`, `src/exposition/`, `src/logger/`)

4. Vérifier la qualité du code :
   ```bash
   uv run just quality-all
   ```

---

## Etape 6 — Commit et push

1. Utiliser des commits conventionnels (commitizen est configuré) :
   - `feat:` pour une nouvelle fonctionnalité
   - `fix:` pour un correctif
   - `docs:` pour de la documentation
   - `refactor:` pour du refactoring
   - `chore:` pour de la maintenance

2. Pousser la branche :
   ```bash
   git push -u origin feat/<issue-number>-<slug-court>
   ```

---

## Etape 7 — Création de la Pull Request

1. Créer la PR ciblant la branche upstream appropriée :
   ```bash
   gh pr create \
     --repo CAprogs/coding-dojo-ia-x-data \
     --base <branche-cible> \
     --title "<type>: <description courte>" \
     --body "$(cat <<'EOF'
   ## Summary
   <description des changements>

   Closes #<issue-number>

   ## Test plan
   - [ ] <checks à vérifier>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

2. Afficher l'URL de la PR à l'utilisateur.

3. Vérifier que la CI passe :
   ```bash
   gh pr checks <pr-number> --repo CAprogs/coding-dojo-ia-x-data --watch
   ```

---

## Règles

- Toujours lire les fichiers avant de les modifier
- Ne jamais push sur `main` ou les branches de mission directement
- Respecter les conventions de commit (conventional commits)
- Vérifier `uv run just quality-all` avant de créer la PR
- Demander confirmation à l'utilisateur avant chaque action visible publiquement (commentaire, PR, push)
