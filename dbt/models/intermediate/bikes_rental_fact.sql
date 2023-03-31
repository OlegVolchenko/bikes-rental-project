{{ config(materialized='view') }}

select
    *
from {{ source('staging','br_trips') }}

