SELECT
    District,
    ST_GEOGFROMTEXT(Geometry) AS Geometry
FROM {{ source('staging','dim_geospatial') }}