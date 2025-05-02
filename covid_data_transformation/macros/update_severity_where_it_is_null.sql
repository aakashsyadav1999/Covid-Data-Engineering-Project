{% macro update_severity_where_it_is_null() %}
    {% set table_schema = 'META_DATA' %}
    {% set table_name = 'COVID_DATA' %}
    {% set column_name = 'SEVERITY_LEVEL' %}

    {% do log("Starting the update_covid_data macro...", info=True) %}

    {% set column_check_query %}
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{{ table_schema }}'
          AND table_name = '{{ table_name }}'
          AND UPPER(column_name) = UPPER('{{ column_name }}')
    {% endset %}

    {% set column_check_result = run_query(column_check_query) %}
    {% set column_exists = column_check_result and column_check_result.columns[0].values() | list | length > 0 %}

    {% if not column_exists %}
        {% do log("Adding SEVERITY_LEVEL column...", info=True) %}
        {% set add_column_query %}
            ALTER TABLE {{ table_schema }}.{{ table_name }}
            ADD COLUMN {{ column_name }} VARCHAR
        {% endset %}
        {% do run_query(add_column_query) %}
    {% else %}
        {% do log("SEVERITY_LEVEL column already exists.", info=True) %}
    {% endif %}

    {% do log("Updating SEVERITY_LEVEL only for NULL values...", info=True) %}
    {% set update_column_query %}
        UPDATE {{ table_schema }}.{{ table_name }}
        SET {{ column_name }} = CASE
            WHEN TOTAL_CONFIRMED_CASES > 100000 THEN 'Severe'
            WHEN TOTAL_CONFIRMED_CASES BETWEEN 50000 AND 100000 THEN 'Moderate'
            ELSE 'Mild'
        END
        WHERE {{ column_name }} IS NULL
    {% endset %}
    {% do run_query(update_column_query) %}

    {% do log("Macro execution completed successfully!", info=True) %}
{% endmacro %}