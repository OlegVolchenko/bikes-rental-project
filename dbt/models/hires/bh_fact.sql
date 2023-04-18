{{ config(
    materialized='table',
    partition_by={
      "field": "start_date",
      "data_type": "datetime",
      "granularity": "day"
    }
    cluster_by = "startstation_borough"
)}}

with hires AS (
SELECT
  rental_id,
  CAST(start_date AS DATETIME) AS start_date,
  CAST(end_date AS DATETIME) AS end_date,
  startstation_name,
  endstation_name
FROM {{ source('staging','trips_export') }}

)
SELECT
  hires.rental_id,
  hires.start_date,
  hires.end_date,
  DATETIME_DIFF(hires.end_date, hires.start_date, MINUTE) AS duration,
  hires.startstation_name,
  hires.endstation_name,
  start_boroughs.borough AS startstation_borough,
  start_boroughs.borough AS endstation_borough
FROM hires
LEFT JOIN {{ ref('dim_boroughs') }} AS start_boroughs ON REPLACE(hires.startstation_name,',','') = start_boroughs.station_name
LEFT JOIN {{ ref('dim_boroughs') }} AS end_boroughs ON REPLACE(hires.startstation_name,',','')  = end_boroughs.station_name
