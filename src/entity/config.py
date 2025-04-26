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

        self.unzip_csv_data:str = os.path.join(
            ARTIFACTS_DIR,UNZIP_DIR_CSV_DATA
        )
    