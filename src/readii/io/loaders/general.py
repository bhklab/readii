import os
import pandas as pd 
import yaml

from typing import Optional, Dict, Union


def loadImageDatasetConfig(dataset_name:str,
                           config_dir_path:str) -> dict:
    """Load the configuration file for a given dataset. Expects the configuration file to be named <dataset_name>.yaml.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset to load the configuration file for.
    config_dir_path : str
        Path to the directory containing the configuration files.

    Returns
    -------
    dict
        Dictionary containing the configuration settings for the dataset.

    Examples
    --------
    >>> config = loadImageDatasetConfig("NSCLC_Radiogenomics", "config/")
    """
    # Make full path to config file
    config_file_path = os.path.join(config_dir_path, f"{dataset_name}.yaml")

    # Check if config file exists
    if os.path.exists(config_file_path):
        # Load the config file
        config = yaml.safe_load(open(config_file_path, "r"))
        return config
    else:
        print(f"Config file {config_file_path} does not exist.")
        return None



def loadFileToDataFrame(file_path:str) -> pd.DataFrame:
    """Load data from a csv or xlsx file into a pandas dataframe.

    Parameters
    ----------
    file_path (str): Path to the data file.

    Returns
    -------
    pd.DataFrame: Dataframe containing the data from the file.
    """
     # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    
    try:
        # Check if the file is an Excel file
        if file_extension == '.xlsx':
            df = pd.read_excel(file_path)
        # Check if the file is a CSV file
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")
        
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None