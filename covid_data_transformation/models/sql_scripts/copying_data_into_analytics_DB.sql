/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml
*/

{{ config(
    materialized='table',
    database='ANALYTICS',
    schema='COPIED_COVID_DATA'
) }}

with source_data as (

    select *
    FROM coviddataset.meta_data.COVID_DATA  -- Fully qualify the schema and table name

)

select *
from source_data

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null