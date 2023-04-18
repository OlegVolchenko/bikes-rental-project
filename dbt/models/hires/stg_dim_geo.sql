SELECT
    District,
    ST_GEOGFROMTEXT(Geometry) AS Geometry
FROM {{ source('staging','trips_export') }}