SELECT
    District,
    ST_GEOGFROMTEXT(Geometry) AS Geometry
FROM {{ ref('dim_geospatial') }}