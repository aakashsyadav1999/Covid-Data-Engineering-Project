{% macro update_covid_data() %}
    {% set table_schema = 'META_DATA' %}
    {% set table_name = 'COVID_DATA' %}
    {% set column_name = 'SEVERITY_LEVEL' %}

    -- Step 1: Check if the column exists
    {% set check_column_query %}
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{{ table_schema }}'
          AND table_name = '{{ table_name }}'
          AND UPPER(column_name) = UPPER('{{ column_name }}')
    {% endset %}

    {% set result = run_query(check_column_query) %}

    {% if result is not none and result.columns[0].values() | length > 0 %}
        {{ log('Column ' ~ column_name ~ ' already exists. Skipping addition.', info=True) }}
    {% else %}
        {{ log('Column ' ~ column_name ~ ' does not exist. Adding column...', info=True) }}

        -- Step 2: Add the column
        {% set add_column_query %}
            ALTER TABLE {{ table_schema }}.{{ table_name }}
            ADD COLUMN {{ column_name }} VARCHAR
        {% endset %}
        {% do run_query(add_column_query) %}
        {{ log('Column ' ~ column_name ~ ' added successfully.', info=True) }}
    {% endif %}

    -- Step 3: Update SEVERITY_LEVEL column based on TOTAL_CONFIRMED_CASES
    {{ log('Updating ' ~ column_name ~ ' column based on TOTAL_CONFIRMED_CASES...', info=True) }}

    {% set update_column_query %}
        UPDATE {{ table_schema }}.{{ table_name }}
        SET {{ column_name }} = CASE
            WHEN TOTAL_CONFIRMED_CASES > 100000 THEN 'Severe'
            WHEN TOTAL_CONFIRMED_CASES BETWEEN 50000 AND 100000 THEN 'Moderate'
            ELSE 'Mild'
        END
    {% endset %}

    {% do run_query(update_column_query) %}
    {{ log('Column ' ~ column_name ~ ' updated successfully based on TOTAL_CONFIRMED_CASES.', info=True) }}
{% endmacro %}
