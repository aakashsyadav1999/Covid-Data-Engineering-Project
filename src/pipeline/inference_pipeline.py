import os
import stat

from src.components.data_fetching import DataFetching
from src.entity.artifact_entity import DataIngestionArtifacts
from src.logger import logging
from src.entity.config import DataFetching
from src.components.data_fetching import DataFetchingSrc

class InitiateInference:
    
    def __init__(self):
        
        self.data_fething_config = DataFetching()
        self.fetch_data = DataFetchingSrc()

    
    def fetching_data(self) -> DataIngestionArtifacts:
        logging.info("Entered the initiate_data_ingestion method of the data ingestion class")
        try:
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