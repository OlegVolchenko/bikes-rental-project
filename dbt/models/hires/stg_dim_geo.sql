SELECT
    District AS borough,
    ST_GEOGFROMTEXT(Geometry) AS geometry,
    population
FROM {{ source('staging','dim_geospatial') }}
LEFT JOIN {{ ref('dim_population') }} AS pop ON District = Borough