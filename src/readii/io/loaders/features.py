from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd

from readii.io.loaders.general import loadFileToDataFrame
from readii.utils import logger


def loadFeatureFilesFromImageTypes(extracted_feature_dir:Union[Path|str], # noqa
                                   image_types:list, 
                                   drop_labels:Optional[bool]=True, 
                                   labels_to_drop:Optional[list]=None)->Dict[str,pd.DataFrame]: 
    """Load in all the specified extracted imaging feature sets from a directory and return them as a dictionary of dataframes.

    Parameters
    ----------
    extracted_feature_dir : str
        Path to the directory containing the extracted feature csv files
    image_types : list, optional
        List of image types to load in. The default is ['original'].
    drop_labels : bool, optional
        Whether to drop the labels from the dataframes. Use when loading labelled data from data_setup_for_modeling.ipynb. The default is True.
    labels_to_drop : list, optional
        List of labels to drop from the dataframes. The default is ["patient_ID","survival_time_in_years","survival_event_binary"] based on code
        in data_setup_for_modeling.ipynb.

    Returns
    -------
    feature_sets : dict
        Dictionary of dataframes containing the extracted radiomics features.
    """
    # Convert directory to Path object if it is a string
    if isinstance(extracted_feature_dir, str):
        extracted_feature_dir = Path(extracted_feature_dir)

    # Set default labels to drop if not specified
    if labels_to_drop is None:
        labels_to_drop = ["patient_ID","survival_time_in_years","survival_event_binary"]

    # Initialize dictionary to store the feature sets
    feature_sets = {}

    # Check if the passed in extracted feature directory exists
    if not extracted_feature_dir.exists() or not extracted_feature_dir.is_dir():
        msg = f"Extracted feature directory {extracted_feature_dir} does not exist."
        logger.error(f"Extracted feature directory {extracted_feature_dir} does not exist.")
        raise FileNotFoundError()
    
    # Get list of all the csv files in the directory with their full paths
    feature_file_list = sorted(extracted_feature_dir.glob("*.csv"))

    # Loop through all the files in the directory
    for image_type in image_types:
        try:
            # Extract the image type feature csv file from the feature directory  
            matching_files = [file for file in feature_file_list if (image_type in file.stem)]  

            match len(matching_files):
                case 1:
                    # Only one file found, use it  
                    pass
                case 0:
                    # No files found for this image type
                    logger.warning(f"No {image_type} feature csv files found in {extracted_feature_dir}")
                    # Skip to the next image type
                    continue
                case _:
                    # Multiple files found
                    msg = f"Multiple {image_type} feature csv files found in {extracted_feature_dir}. First one will be used."
                    logger.warning(msg)

            feature_file_path = matching_files[0]  
            # Remove the image type file from the list of feature files  
            feature_file_list.remove(feature_file_path)

        except Exception as e:
            logger.warning(f"Error loading {image_type} feature csv files from {extracted_feature_dir}: {e}")
            raise e
            
        # Load the feature data into a pandas dataframe
        raw_feature_data = loadFileToDataFrame(feature_file_path)

        try:
            # Drop the labels from the dataframe if specified
            if drop_labels:
                # Data is now only extracted features
                raw_feature_data.drop(labels_to_drop, axis=1, inplace=True)

        except KeyError:
            logger.warning(f"{feature_file_path} does not have the labels {labels_to_drop} to drop.")
            # Skip to the next image type
            continue

        # Save the dataframe to the feature_sets dictionary
        feature_sets[image_type] = raw_feature_data
    # end image type loop

    # After processing all image types, check if any feature sets were loaded 
    if not feature_sets:
        logger.error(f"No valid feature sets were loaded from {extracted_feature_dir}")
        raise ValueError()
    
    return feature_sets