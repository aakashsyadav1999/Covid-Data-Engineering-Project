import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

ARTIFACTS_DIR = os.path.join("artifacts")
LOGS_DIR = "logs"
LOGS_FILE_NAME = "SIDFC.log"


# Data Ingestion 
ROOT_DIR= "DataFetchArtifacts"
SOURCE_URL= "https://drive.google.com/file/d/1qrlF01WOC210RfPm3jdSnU6sG_hew7aM/view?usp=sharing"
UNZIP_DIR= ROOT_DIR
LOCAL_FILE_PATH = "sample_submission.zip"
UNZIP_DIR_CSV_DATA = "DataTransformationArtifacts"
