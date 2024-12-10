from pathlib import Path
from typing import Union

def getImageTypesFromDirectory(raw_data_dir:Union[Path|str],
                               feature_file_prefix:str = "",
                               feature_file_suffix:str = ".csv"):
    """ Function to get a list of image types from a directory containing image feature files.

    Parameters
    ----------
    raw_data_dir : str
        Path to the directory containing the image feature files.
    feature_file_prefix : str, optional
        Prefix to remove from the feature file name. The default is "".
    feature_file_suffix : str, optional
        Suffix to remove from the feature file name. The default is ".csv".
    
    Returns
    -------
    list
        List of image types from the image feature files.
    """
    # Check if raw_data_dir is a string or a Path object, convert to Path object if it is a string
    if isinstance(raw_data_dir, str):
        raw_data_dir = Path(raw_data_dir)

    # Check if the directory exists
    if not raw_data_dir.exists():
        raise FileNotFoundError(f"Directory {raw_data_dir} does not exist.")
    
    # Check if the directory is a directory
    if not raw_data_dir.is_dir():
        raise NotADirectoryError(f"Path {raw_data_dir} is not a directory.")
    
    # Check that directory contains files with the specified prefix and suffix
    if not any(raw_data_dir.glob(f"{feature_file_prefix}*{feature_file_suffix}")):
        raise FileNotFoundError(f"No files with prefix {feature_file_prefix} and suffix {feature_file_suffix} found in directory {raw_data_dir}.")

    # Initialize an empty list to store the image types
    image_types = []

    # Get list of file banes with the specified prefix and suffix in the directory
    for file in raw_data_dir.glob(f"{feature_file_prefix}*{feature_file_suffix}"):
        file_name = file.name

        # Remove the prefix and suffix from the file name
        image_type = file_name.removeprefix(feature_file_prefix).removesuffix(feature_file_suffix)
        
        # Add the image type to the list
        image_types.append(image_type)

    return image_types