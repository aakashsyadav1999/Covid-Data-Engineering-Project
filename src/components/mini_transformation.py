from dataclasses import dataclass
import time
import os
from src.entity.config import MiniDataTransformationConfig
from src.logger import logging
import pandas as pd


class MiniDataTransformation:
    
    def __init__(self):
        
        self.mini_transformation_config = MiniDataTransformationConfig()
    
    def mini_transformation(self,raw_data):
        """
        This function is used to perform mini transformation on the data
        """
        try:
            logging.info("Entered the mini_transformation method of the data transformation class")
            # Perform mini transformation on the data
            
            # Load the raw data into a DataFrame
            data = pd.read_csv(raw_data)
            
            # Rename the column
            data.rename(columns={
                "Name of State / UT": "NAME_OF_STATE",
                "Total Confirmed cases": "TOTAL_CONFIRMED_CASES",
                "Cured/Discharged/Migrated": "CURED_DISCHARGED_MIGRATED",
                "New cases": "NEW_CASES",
                "New deaths": "NEW_DEATHS",
                "New recovered": "NEW_RECOVERED",
            }, inplace=True)
            
            # Save the transformed data back to a CSV file
            transformed_data_path = os.path.join(self.mini_transformation_config.data_transformation_artifacts_dir, "transformed_data.csv")
            data.to_csv(transformed_data_path, index=False)
            
            logging.info("Mini transformation completed successfully")
            return transformed_data_path
        except Exception as e:
            error_message = f"Error occurred during mini transformation: {e}"
            logging.error(error_message)
            #raise NerException(error_message)
        finally:
            logging.info("Exiting the mini_transformation method of the data transformation class")
            # Clean up any temporary files or resources if needed
            # os.remove(raw_data)  # Remove the raw data file if needed
            
            

