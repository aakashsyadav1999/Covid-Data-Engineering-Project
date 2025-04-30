# Use Astronomer Airflow runtime base image
FROM quay.io/astronomer/astro-runtime:12.8.0

# Set the working directory inside the container
WORKDIR /opt/airflow

# Copy requirements first for caching
COPY requirements.txt .

# Install system packages and Python environment tools
USER root
RUN apt-get update && apt-get install -y python3 python3-venv && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install Python dependencies
RUN python3 -m venv /opt/airflow/venv
RUN /bin/bash -c "source /opt/airflow/venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Copy all necessary files (your DAGs, scripts, etc.)
COPY dags/ ./dags/
COPY . .
COPY main.py ./python/main.py

# Ensure correct permissions
RUN chown -R astro:astro /opt/airflow
USER astro

# Default command (will be overridden by Airflow runtime)
CMD ["airflow", "standalone"]
