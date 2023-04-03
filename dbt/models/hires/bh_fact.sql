{{ config(materialized='view') }}

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
  rental_id,
  start_date,
  end_date,
  DATETIME_DIFF(end_date, start_date, MINUTE) AS duration,
  startstation_name,
  endstation_name
FROM hires
