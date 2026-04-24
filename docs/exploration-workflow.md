# Workflow d'exploration avec Claude Code

Guide concret pour inspecter les tables du warehouse et poser des questions à Claude Code sur la donnée.

## Prérequis

- Pipeline exécuté au moins une fois (`uv run just final-workflow`)
- `warehouse/prod.duckdb` présent
- Claude Code installé (`claude` disponible en CLI)

## Structure du warehouse

Le warehouse suit une architecture medallion en trois couches :

| Couche | Table | Description |
|--------|-------|-------------|
| **Bronze** | `raw_events` | Données brutes issues de l'API Que Faire à Paris |
| **Silver** | `filtered_rows` | Lignes filtrées (doublons supprimés) |
| **Silver** | `agenda` | Événements avec créneaux explodés |
| **Silver** | `agenda_enriched` | Enrichissement accessibilité + géocodage |
| **Silver** | `up_to_date_events` | Événements à venir (filtre temporel) |
| **Gold** | `today_events` | Événements du jour |
| **Gold** | `nb_events_by_tags` | Comptage par tag |
| **Gold** | `handicap_friendly_events` | Événements accessibles PMR |

> Les tables gold sont le point d'entrée naturel pour explorer la donnée métier.

## Commandes d'exploration

```bash
# Ouvrir un shell DuckDB sur le warehouse (sans relancer dbt)
uv run just explore

# Ouvrir l'interface graphique DuckDB (après dbt run)
uv run just duckdb-ui

# Générer et consulter la documentation dbt
uv run just dbt-catalog
```

### Requêtes DuckDB utiles en shell interactif

```sql
-- Lister toutes les tables du warehouse
SHOW TABLES;

-- Inspecter le schéma d'une table
DESCRIBE today_events;

-- Aperçu rapide des données
SELECT * FROM today_events LIMIT 5;

-- Compter les événements par tag (top 10)
SELECT * FROM nb_events_by_tags LIMIT 10;

-- Vérifier la fraîcheur des données
SELECT min(date_start), max(date_start), count(*) FROM up_to_date_events;
```

## Parcours d'exploration avec Claude Code

### 1. Démarrer Claude Code dans le projet

```bash
claude
```

### 2. Questions types à poser

**Sur le schéma et la structure :**
```
Quelles sont les colonnes de la table today_events dans warehouse/prod.duckdb ?
```

```
Explique la différence entre up_to_date_events et today_events en lisant les fichiers SQL dans src/transformation/.
```

**Sur la donnée :**
```
Lis le fichier src/transformation/dbt_paris_event_analyzer/models/gold/today_events.sql
et explique quels filtres sont appliqués.
```

```
Dans src/transformation/dbt_paris_event_analyzer/models/silver/agenda_enriched.sql,
comment est calculé le champ is_handicap_friendly ?
```

**Sur le pipeline :**
```
Décris le chemin complet d'une donnée depuis l'API Paris Open Data jusqu'à la table gold today_events.
```

### 3. Inspecter le warehouse directement

Claude Code peut lire et exécuter du SQL sur le warehouse avec le Bash tool :

```
Lance `duckdb warehouse/prod.duckdb -c "SELECT count(*) FROM today_events"`
et dis-moi combien d'événements sont disponibles aujourd'hui.
```

## Points d'entrée recommandés

| Objectif | Par où commencer |
|----------|-----------------|
| Comprendre la donnée métier | Tables gold (`today_events`, `nb_events_by_tags`) |
| Déboguer une transformation | Modèles silver dans `src/transformation/.../models/silver/` |
| Vérifier les sources | Bronze `raw_events` + fichier `endpoints.json` |
| Explorer visuellement | `uv run just duckdb-ui` ou `uv run just dbt-catalog` |
