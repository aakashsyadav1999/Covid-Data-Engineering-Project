import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402
from typing import Tuple, Dict, Any
import pandas as pd
from src.exception import CustomException
from src.logger import logging



class DataTransformation:
    
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def drop_columns(self, columns: list) -> pd.DataFrame:
        """
        Drop specified columns from the DataFrame.

        Args:
            columns (list): List of column names to drop.

        Returns:
            pd.DataFrame: DataFrame with specified columns dropped.
        """
        try:
            self.data.drop(columns=columns, inplace=True)
            return self.data
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def fill_missing_values(self, strategy: str = 'mean') -> pd.DataFrame:
        
        """
        Fill missing values in the DataFrame using the specified strategy.

        Args:
            strategy (str): Strategy to use for filling missing values. Options are 'mean', 'median', 'mode'.

        Returns:
            pd.DataFrame: DataFrame with missing values filled.
        """
        try:
            if strategy == 'mean':
                self.data.fillna(self.data.mean(), inplace=True)
            elif strategy == 'median':
                self.data.fillna(self.data.median(), inplace=True)
            elif strategy == 'mode':
                self.data.fillna(self.data.mode().iloc[0], inplace=True)
            else:
                raise ValueError("Invalid strategy. Choose from 'mean', 'median', or 'mode'.")
            return self.data
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def return_transformed_data(self) -> pd.DataFrame:
        """
        Return the transformed DataFrame.

        Returns:
            pd.DataFrame: Transformed DataFrame.
        """
        try:
            return self.data
        except Exception as e:
            raise CustomException(e, sys) from e