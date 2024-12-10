import os
import pandas as pd 
import yaml


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
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file {config_file_path} does not exist.")
    
    try:
        # Load the config file
        with open(config_file_path, "r") as f:
            return yaml.safe_load(f)

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {e}")  
def loadFileToDataFrame(file_path:str) -> pd.DataFrame:
    """Load data from a csv or xlsx file into a pandas dataframe.

    Parameters
    ----------
    file_path (str): Path to the data file.

    Returns
    -------
    pd.DataFrame: Dataframe containing the data from the file.
    """
    if not file_path:
        raise ValueError("file_path cannot be empty")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")

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
        
        if df.empty:
            raise ValueError("Loaded DataFrame is empty")
        
        return df
    
    except pd.errors.EmptyDataError:
        raise ValueError("File is empty")
    except (pd.errors.ParserError, ValueError) as e:
        raise ValueError(f"Error parsing file: {e}")