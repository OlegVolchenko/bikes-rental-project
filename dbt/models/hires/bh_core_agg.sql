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
    fact.year,
    fact.borough,
    fact.avg_duration,
    fact.hires,
    geo.geometry,
    geo.population,
FROM fact
LEFT JOIN {{ ref('stg_dim_geo') }} AS geo USING(borough)
