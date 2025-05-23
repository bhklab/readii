from pathlib import Path
from typing import Dict, Union

from readii.io.loaders import loadImageDatasetConfig
from readii.utils import logger

def get_full_data_name(config: Union[Dict | Path]):
    """Combine DATA_SOURCE and DATASET_NAME config variables into a single string."""
    
    match type(config):
        case Path():
            dataset_config = loadImageDatasetConfig(config.stem, config.parent)
        case Dict():
            dataset_config = config
        case _:
            message = "Error getting full data name: config must be of type Path or Dict."
            logger.debug(message)
            raise TypeError(message) 

    try:
        data_source = dataset_config['DATA_SOURCE']
        dataset_name = dataset_config['DATASET_NAME']
        return f"{data_source}_{dataset_name}"
    except KeyError as e:
        message = f"Missing required key in dataset configuration: {e}"
        logger.error(message)
        raise ValueError(message) from e