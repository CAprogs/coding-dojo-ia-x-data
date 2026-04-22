with qfap_tags_analysis as (
  SELECT
    string_agg(qfap_tags, ';' ORDER BY qfap_tags ASC) as qfap_tags_agg,
    regexp_split_to_array(qfap_tags_agg, ';') AS qfap_tags_list,
  FROM {{ ref('up_to_date_events') }}
)
SELECT
    qfap_tags_distinct,
    count(*) as nb_events
From qfap_tags_analysis, unnest(qfap_tags_list) as t(qfap_tags_distinct)
group by qfap_tags_distinct
ORDER BY nb_events DESC
