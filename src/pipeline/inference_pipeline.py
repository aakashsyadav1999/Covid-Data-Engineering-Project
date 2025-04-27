import os
import stat

from src.components.data_fetching import DataFetching
from src.entity.artifact_entity import DataIngestionArtifacts
from src.logger import logging
from src.entity.config import DataFetching, MiniDataTransformationConfig, SnowflakeConfig
from src.components.data_fetching import DataFetchingSrc
from src.components.mini_transformation import MiniDataTransformation
from src.components.load_data_snowflake import SnowflakeLoader

import pandas as pd

class InitiateInference:
    
    def __init__(self):
        
        self.data_fething_config = DataFetching()
        self.fetch_data = DataFetchingSrc()
        self.mini_transformation_config = MiniDataTransformationConfig()
        self.mini_transformation = MiniDataTransformation()
        self.snowflake_config = SnowflakeConfig()
        self.snowflake_loader = SnowflakeLoader()

    
    def fetching_data(self) -> DataIngestionArtifacts:
        logging.info("Entered the initiate_data_ingestion method of the data ingestion class")
        try:
            # if artifact folder is not created then create it
            if not os.path.exists(self.data_fething_config.data_ingestion_artifacts_dir):
                os.makedirs(self.data_fething_config.data_ingestion_artifacts_dir, exist_ok=True)
                logging.info(f"Creating directory {self.data_fething_config.data_ingestion_artifacts_dir}")
            
            
            os.chmod(self.data_fething_config.data_ingestion_artifacts_dir,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            logging.info(f"Creating {(self.data_fething_config.data_ingestion_artifacts_dir)} directory")

            #Downloading data from given URL
            self.fetch_data.fetch_data_from_gdrive()
            logging.info(f"Downloading data from given url {self.data_fething_config.source_url}")

            #extract file
            self.fetch_data.extract_zip_file()
            logging.info(f"Extracting file in directory {self.data_fething_config.data_ingestion_artifacts_dir}")

        except Exception as e:
            raise e
        
    def transform_data(self) -> str:
        logging.info("Entered the mini_transformation method of the data transformation class")
        try:
            # Read the data from the CSV file from the CSV file is located in the directory where the zip file was extracted
           
            data_path = os.path.join(self.data_fething_config.unzip_csv_data, "complete.csv")
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"No such file or directory: '{data_path}'")
            
            # Perform mini transformation on the data
            transformed_data_path = self.mini_transformation.mini_transformation(data_path)
            logging.info("Mini transformation completed successfully")
            return transformed_data_path
        except Exception as e:
            error_message = f"Error occurred during mini transformation: {e}"
            logging.error(error_message)
            #raise NerException(error_message)
        finally:
            logging.info
            
    def load_data_to_snowflake(self, transformed_data_path: str) -> None:
        logging.info("Entered the load_data_to_snowflake method of the snowflake loader class")
        try:
            # Load the transformed data to Snowflake
            self.snowflake_loader.load_data_to_snowflake(transformed_data_path)
            logging.info("Data loaded to Snowflake successfully")
        except Exception as e:
            error_message = f"Error occurred while loading data to Snowflake: {e}"
            logging.error(error_message)
            #raise NerException(error_message)
        finally:
            logging.info("Exiting the load_data_to_snowflake method of the snowflake loader class")