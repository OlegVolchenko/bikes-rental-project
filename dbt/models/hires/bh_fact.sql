{{ config(materialized='view') }}

SELECT
  rental_id,
  CAST(start_date AS DATETIME) AS start_date,
  CAST(start_date AS DATETIME) AS start_date,
  DATETIME_DIFF(end_date, start_date, MINUTE) AS duration,
  startstation_name,
  endstation_name
FROM {{ source('staging','trips_export') }}
