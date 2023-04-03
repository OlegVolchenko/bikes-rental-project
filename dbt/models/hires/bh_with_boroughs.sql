SELECT
    fact.rental_id,
    fact.start_date,
    fact.end_date,
    fact.duration,
    fact.startstation_name,
    start_boroughs.borough AS startstation_borough,
    fact.endstation_name,
    start_boroughs.borough AS endstation_borough
FROM {{ ref('bh_fact') }} AS fact
LEFT JOIN {{ ref('dim_boroughs') }} AS start_boroughs ON REPLACE(fact.startstation_name,',','') = start_boroughs.station_name
LEFT JOIN {{ ref('dim_boroughs') }} AS end_boroughs ON REPLACE(fact.startstation_name,',','')  = end_boroughs.station_name