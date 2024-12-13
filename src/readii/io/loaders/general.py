from pathlib import Path

import pandas as pd
import yaml


class ConfigError(Exception):
    """Base class for errors in the config module."""

    pass

class DataFrameLoadError(Exception):
    """Custom exception for DataFrame loading errors."""

    pass

def loadImageDatasetConfig(dataset_name: str, config_dir_path: str | Path) -> dict:
    """Load the configuration file for a given dataset.

    Expects the configuration file to be named <dataset_name>.yaml.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset to load the configuration file for.
    config_dir_path : str or pathlib.Path
        Path to the directory containing the configuration files.

    Returns
    -------
    dict
        Dictionary containing the configuration settings for the dataset.

    Examples
    --------
    >>> config = loadImageDatasetConfig("NSCLC_Radiogenomics", "config")
    """
    config_dir_path = Path(config_dir_path)
    config_file_path = config_dir_path / f"{dataset_name}.yaml"

    if not config_file_path.exists():
        msg = f"Config file {config_file_path} does not exist."
        raise FileNotFoundError(msg)
    
    try:
        with config_file_path.open("r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as ye:
        raise ConfigError("Invalid YAML in config file") from ye

    if not config:
        raise ConfigError("Config file is empty or invalid")

    return config



def loadFileToDataFrame(file_path: str | Path) -> pd.DataFrame:
    """Load data from a csv or xlsx file into a pandas dataframe.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the data file.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the data from the file.
    """
    file_path = Path(file_path)
    if not file_path:
        raise ValueError("File is empty")

    if not file_path.exists():
        msg = f"File {file_path} does not exist"
        raise FileNotFoundError(msg)

    # Get the file extension
    file_extension = file_path.suffix

    try:
        if file_extension == '.xlsx':
            df = pd.read_excel(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            msg = f"Unsupported file format {file_extension}. Please provide a .csv or .xlsx file."
            raise ValueError(msg)

    except pd.errors.EmptyDataError as e:
        raise DataFrameLoadError("File is empty") from e

    except (pd.errors.ParserError, ValueError) as e:
        raise DataFrameLoadError("Error parsing file") from e

    if df.empty:
        raise DataFrameLoadError("Dataframe is empty")
    return df