select
    *
from {{ source('staging','trips_export') }}

