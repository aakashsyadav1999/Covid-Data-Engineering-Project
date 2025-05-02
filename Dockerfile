# Use the official Apache Airflow image
FROM apache/airflow:3.0.0
 
# Set Airflow home
ENV AIRFLOW_HOME=/opt/airflow
 
# Add `src` to PYTHONPATH
ENV PYTHONPATH="${AIRFLOW_HOME}/src:${PYTHONPATH}"
 
# Copy everything into container
COPY . ${AIRFLOW_HOME}/
 
# Upgrade pip (recommended) as the `airflow` user
USER airflow
RUN pip install --upgrade pip
 
# Install all Python dependencies as the `airflow` user
RUN pip install --no-cache-dir -r ${AIRFLOW_HOME}/requirements.txt