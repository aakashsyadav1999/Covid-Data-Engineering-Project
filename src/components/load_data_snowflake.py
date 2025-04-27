import pandas as pd
import snowflake.connector
from src.entity.config import SnowflakeConfig

# This code is part of a data pipeline that loads data into Snowflake.
class SnowflakeLoader:
    
    # This class is responsible for loading data into Snowflake.
    def __init__(self):
        self.config = SnowflakeConfig()

    # Connect to Snowflake using the provided credentials and configuration.
    def connect_to_snowflake(self):
        conn = snowflake.connector.connect(
            user=self.config.snowflake_user,
            password=self.config.snowflake_password,
            account=self.config.snowflake_account,
            warehouse=self.config.snowflake_warehouse,
            database=self.config.snowflake_database,
            schema=self.config.snowflake_schema
        )
        return conn
    
    # Load data from a CSV file into Snowflake.
    def load_data_to_snowflake(self, file_path):
        conn = self.connect_to_snowflake()
        cursor = conn.cursor()
        try:
            # Read data from CSV file
            data = pd.read_csv(file_path)
            
            # Create a temporary stage
            cursor.execute("CREATE OR REPLACE TEMPORARY STAGE temp_stage")
            
            # Add missing column if necessary
            if 'EXTRA_COLUMN' not in data.columns:
                data['EXTRA_COLUMN'] = None  # Or provide a default value
            
            # Write data to Snowflake stage
            data.to_csv('temp_data.csv', index=False)
            with open('temp_data.csv', 'rb') as file:
                cursor.execute("PUT file://temp_data.csv @temp_stage")
            
            # Copy data from stage to table
            cursor.execute(f"""
                COPY INTO {self.config.snowflake_table}
                FROM @temp_stage/temp_data.csv
                FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
            """)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
        finally:
            cursor.close()
            conn.close()