from dataclasses import dataclass
import time
import os
from zipfile import ZipFile
from pathlib import Path
import urllib.request as request
import requests
import zipfile
import stat
import gdown
from src.entity.config import DataFetching
from src.logger import logging


class DataFetchingSrc:
    
    def __init__(self):
        self.data_fething_config = DataFetching()
    
    def fetch_data_from_gdrive(self):
        
        '''
        Fetch data from the url
        '''

        try: 
            dataset_url = self.data_ingestion_config.source_url
            zip_download_dir = self.data_ingestion_config.local_data_file
            if not os.path.exists(self.data_ingestion_config.data_ingestion_artifacts_dir):
                logging.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            print(prefix+file_id,zip_download_dir)
            gdown.download(prefix+file_id,zip_download_dir)

            logging.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            raise e  
        
    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        """
        unzip_path = self.data_ingestion_config.unzip_csv_data
        os.makedirs(unzip_path, exist_ok=True)
        try:
            zip_file_path = self.data_ingestion_config.local_data_file
            if not os.path.exists(zip_file_path):
                raise FileNotFoundError(f"No such file or directory: '{zip_file_path}'")
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            logging.info(f"Extracted file to directory: {unzip_path}")
        except FileNotFoundError as e:
            error_message = f"File not found: {e}"
            logging.error(error_message)
            #raise NerException(error_message)
        except zipfile.BadZipFile as e:
            error_message = f"Bad zip file: {e}"
            logging.error(error_message)
            #raise NerException(error_message)
        except Exception as e:
            error_message = f"Error occurred during zip extraction: {e}"
            logging.error(error_message)
            #raise NerException(error_message)
            
    
            
        