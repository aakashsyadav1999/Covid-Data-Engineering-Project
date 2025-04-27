from dataclasses import dataclass
import os
from pathlib import Path

from src.constant import *


@dataclass
class DataFetching:
    
    def __init__ (self):
        self.data_ingestion_artifacts_dir:str = os.path.join(
            ARTIFACTS_DIR,ROOT_DIR
        )
        self.source_url:str = SOURCE_URL
        self.unzip_dir:str = UNZIP_DIR
        self.local_data_file:str = os.path.join(
            self.data_ingestion_artifacts_dir,LOCAL_FILE_PATH
        )
        self.unzip_csv_data:str = os.path.join(
            ARTIFACTS_DIR,UNZIP_DIR_CSV_DATA
        )
        
@dataclass       
class MiniDataTransformationConfig:
    
    def __init__(self):
        self.data_transformation_artifacts_dir:str = os.path.join(
            ARTIFACTS_DIR,UNZIP_DIR_CSV_DATA
        )
        self.transformed_data:str = os.path.join(
            self.data_transformation_artifacts_dir,"transformed_data.csv"
        )
    
@dataclass
class SnowflakeConfig:
    
    def __init__(self):
        self.snowflake_account:str = SNOWFLAKE_ACCOUNT
        self.snowflake_user:str = SNOWFLAKE_USER
        self.snowflake_password:str = SNOWFLAKE_PASSWORD
        self.snowflake_warehouse:str = SNOWFLAKE_WAREHOUSE
        self.snowflake_database:str = SNOWFLAKE_DATABASE
        self.snowflake_schema:str = SNOWFLAKE_SCHEMA
        self.snowflake_table:str = SNOWFLAKE_TABLE