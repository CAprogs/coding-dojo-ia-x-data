---
name: contribute
description: Guide et automatise le flux de contribution au repo (fork, sync, branche, PR). Utiliser quand un contributeur veut travailler sur une issue ou soumettre une PR.
argument-hint: [issue-number]
arguments: [issue]
allowed-tools: Bash(git *) Bash(gh *)
---

# Flux de contribution

Tu guides le contributeur dans le workflow de contribution au repo upstream `CAprogs/coding-dojo-ia-x-data`.

## Etape 1 - Vérifier le setup

Vérifie que le remote `upstream` pointe vers `CAprogs/coding-dojo-ia-x-data` :

```bash
git remote -v
```

Si `upstream` n'existe pas, ajoute-le :

```bash
git remote add upstream https://github.com/CAprogs/coding-dojo-ia-x-data.git
```

## Etape 2 - Synchroniser avec upstream

Récupère les dernières modifications du repo de Charles et mets à jour la branche `main` locale :

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Etape 3 - Récupérer l'issue

Si un numéro d'issue est fourni (`$issue`), récupère ses détails :

```bash
gh issue view $issue --repo CAprogs/coding-dojo-ia-x-data
```

Affiche un résumé de l'issue au contributeur (titre, description, labels, assignee).

Si aucun numéro n'est fourni, liste les issues ouvertes disponibles :

```bash
gh issue list --repo CAprogs/coding-dojo-ia-x-data --state open
```

Demande au contributeur quelle issue il veut traiter.

## Etape 4 - Créer la branche de travail

Crée une branche nommée d'après l'issue depuis `main` à jour :

```bash
git checkout -b issue-$issue main
```

## Etape 5 - Développement

Informe le contributeur qu'il peut maintenant travailler sur sa branche. Rappelle-lui de :
- Faire des commits atomiques et clairs
- Référencer l'issue dans les messages de commit (ex: `refs #$issue`)

## Etape 6 - Pousser et créer la PR

Une fois le travail terminé, pousse la branche sur le fork et crée une PR vers upstream :

```bash
git push origin issue-$issue
```

Puis crée la PR avec `gh` :

```bash
gh pr create --repo CAprogs/coding-dojo-ia-x-data \
  --head <user>:issue-$issue \
  --base main \
  --title "<titre descriptif>" \
  --body "Closes CAprogs/coding-dojo-ia-x-data#$issue

## Résumé
<description des changements>

## Tests
<comment tester>"
```

Demande confirmation au contributeur avant de créer la PR.

## Etape 7 - Suivi

Informe le contributeur que :
- La PR est en attente de review par les mainteneurs
- Il peut suivre l'état de la PR avec `gh pr status`
- Après merge, il devra resynchroniser son fork (reprendre à l'étape 2)
