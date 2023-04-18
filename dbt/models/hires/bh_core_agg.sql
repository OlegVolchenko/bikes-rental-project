{{ config(materialized='table') }}

WITH fact AS (
SELECT
    EXTRACT(YEAR FROM start_date) AS year,
    startstation_borough AS borough,
    AVG(duration) AS avg_duration,
    COUNT(DISTINCT rental_id) AS hires
FROM {{ ref('bh_fact') }}
GROUP BY 1,2 )
SELECT
    year,
    borough,
    avg_duration,
    hires,
    geo.Geometry,
    pop.Population,
FROM fact
LEFT JOIN {{ ref('stg_dim_geo') }} AS geo ON fact.borough = geo.District
LEFT JOIN {{ ref('dim_population') }} AS pop ON fact.borough = pop.Borough
