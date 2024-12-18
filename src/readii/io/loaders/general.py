from pathlib import Path

import pandas as pd
import yaml

from readii.utils import logger


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
        logger.error(msg)
        raise FileNotFoundError()
    
    try:
        with config_file_path.open("r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as ye:
        msg = f"Invalid YAML config file for {dataset_name}."
        logger.exception(msg)
        raise ConfigError() from ye

    if not config:
        msg = f"{dataset_name} config file is empty or invalid."
        logger.error(msg)
        raise ConfigError()

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
        msg = f"File {file_path} is empty"
        logger.error(msg)
        raise ValueError()

    if not file_path.exists():
        msg = f"File {file_path} does not exist"
        logger.error(msg)
        raise FileNotFoundError()

    # Get the file extension
    file_extension = file_path.suffix

    try:
        if file_extension == '.xlsx':
            df = pd.read_excel(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            msg = f"Unsupported file format {file_extension}. Please provide a .csv or .xlsx file."
            logger.exception(msg)
            raise ValueError()

    except pd.errors.EmptyDataError as e:
        msg = f"File {file_path} is empty"
        logger.exception(msg)
        raise DataFrameLoadError() from e

    except (pd.errors.ParserError, ValueError) as e:
        msg = "Error pargins {file_path}"
        logger.exception(msg)
        raise DataFrameLoadError() from e

    if df.empty:
        msg = "Loaded Dataframe is empty"
        logger.exception(msg)
        raise DataFrameLoadError()
    
    return df