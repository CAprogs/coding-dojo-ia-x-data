WITH exploded AS (
  SELECT
    id,
    fragment
  FROM {{ ref('filtered_rows') }},
  UNNEST(regexp_split_to_array(occurrences, ';')) AS t(fragment)
),
parsed AS (
  SELECT
    id,
    timezone('Europe/London', regexp_extract(fragment, '([^_]+)_([^_]+)', 1)::TIMESTAMPTZ) AS start_ts, -- LONDON timezone is used because the timezone is not aligned with the event's date description
    timezone('Europe/London', regexp_extract(fragment, '([^_]+)_([^_]+)', 2)::TIMESTAMPTZ) AS end_ts
  FROM exploded
)
SELECT
  id,
  list(
    struct_pack(start_time := start_ts, end_time := end_ts)
  ) AS tous_les_creneaux,
  len(tous_les_creneaux) as nb_total_occurences,
  list_filter(tous_les_creneaux, lambda x: x['start_time'] > current_localtimestamp()) as prochains_creneaux,
  [x['start_time']::DATE for x in prochains_creneaux] as next_start_date,
  CASE WHEN current_date() in next_start_date THEN TRUE ELSE FALSE END as has_event_today,
  len(prochains_creneaux) as nb_next_occurrences
FROM parsed
GROUP BY id
