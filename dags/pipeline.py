from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator  # Import BashOperator
from datetime import datetime
import logging
import os
import sys

# Set the project root dynamically for Docker
project_root = os.getenv('PROJECT_ROOT', '/opt/airflow')  # Default to /opt/airflow in Docker
sys.path.append(os.path.join(project_root, 'src'))

from src.pipeline.inference_pipeline import InitiateInference

# Initialize the inference pipeline
inference = InitiateInference()

def fetch_data_task():
    try:
        logging.info("Starting data fetching...")
        data_ingestion_artifacts = inference.fetching_data()
        logging.info("Data fetching completed.")
        return data_ingestion_artifacts
    except Exception as e:
        logging.error(f"Error in data fetching: {e}")
        raise

def transform_data_task(**kwargs):
    try:
        logging.info("Starting data transformation...")
        transformed_data_path = inference.transform_data()
        logging.info(f"Data transformation completed. Transformed data path: {transformed_data_path}")
        return transformed_data_path
    except Exception as e:
        logging.error(f"Error in data transformation: {e}")
        raise

def load_data_to_snowflake_task(**kwargs):
    try:
        # Get the transformed data path from the previous task
        ti = kwargs['ti']
        transformed_data_path = ti.xcom_pull(task_ids='transform_data_task')
        logging.info("Starting data loading to Snowflake...")
        inference.load_data_to_snowflake(transformed_data_path)
        logging.info("Data loading to Snowflake completed.")
    except Exception as e:
        logging.error(f"Error in loading data to Snowflake: {e}")
        raise

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    dag_id='inference_pipeline_dag',
    default_args=default_args,
    catchup=False,
)

# Define the tasks
fetch_data = PythonOperator(
    task_id='fetch_data_task',
    python_callable=fetch_data_task,
    dag=dag
)

transform_data = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data_task,
    dag=dag
)

load_data_to_snowflake = PythonOperator(
    task_id='load_data_to_snowflake_task',
    python_callable=load_data_to_snowflake_task,
    dag=dag
)

# Add a BashOperator to run the dbt command
run_dbt_model = BashOperator(
    task_id='run_dbt_model_task',
    bash_command='cd /opt/airflow/covid_Data_transformation && dbt run --select copying_data_into_analytics_DB',
    dag=dag
)


# Add a BashOperator to run the dbt command
update_severity_where_it_null = BashOperator(
    task_id='update_severity_where_it_null_task',
    bash_command='cd /opt/airflow/covid_Data_transformation && dbt run-operation update_severity_where_it_is_null',
    dag=dag
)


# Set task dependencies
fetch_data >> transform_data >> load_data_to_snowflake >> run_dbt_model >> update_severity_where_it_null