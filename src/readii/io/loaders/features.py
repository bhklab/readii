import os
import pandas as pd 

from typing import Optional, Dict

from readii.io.loaders.general import loadFileToDataFrame

from readii.utils import logger


def loadFeatureFilesFromImageTypes(extracted_feature_dir:str,
                                   image_types:list, 
                                   drop_labels:Optional[bool]=True, 
                                   labels_to_drop:Optional[list]=None)->Dict[str,pd.DataFrame]:
    """Function to load in all the extracted imaging feature sets from a directory and return them as a dictionary of dataframes.

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
    # Set default labels to drop if not specified
    if labels_to_drop is None:
        labels_to_drop = ["patient_ID","survival_time_in_years","survival_event_binary"]

    # Initialize dictionary to store the feature sets
    feature_sets = {}

    # Check if the passed in extracted feature directory exists
    if not os.path.isdir(extracted_feature_dir):
        raise FileNotFoundError(f"Extracted feature directory {extracted_feature_dir} does not exist.")
    
    feature_file_list = os.listdir(extracted_feature_dir)

    # Loop through all the files in the directory
    for image_type in image_types:
        try:
            # Extract the image type feature csv file from the feature directory  
            matching_files = [file for file in feature_file_list if (image_type in file) and (file.endswith(".csv"))]  
            if matching_files:  
                image_type_feature_file = matching_files[0]  
                # Remove the image type file from the list of feature files  
                feature_file_list.remove(image_type_feature_file)
        except IndexError as e:
            logger.warning(f"No {image_type} feature csv files found in {extracted_feature_dir}")
            # Skip to the next image type
            continue


        # Get the full path to the feature file
        feature_file_path = os.path.join(extracted_feature_dir, image_type_feature_file)
            
        # Load the feature data into a pandas dataframe
        raw_feature_data = loadFileToDataFrame(feature_file_path)

        try:
            # Drop the labels from the dataframe if specified
            if drop_labels:
                # Data is now only extracted features
                raw_feature_data.drop(labels_to_drop, axis=1, inplace=True)
        except KeyError as e:
            logger.warning(f"{feature_file_path} does not have the labels {labels_to_drop} to drop.")
            # Skip to the next image type
            continue

        # Save the dataframe to the feature_sets dictionary
        feature_sets[image_type] = raw_feature_data

    # After processing all image types, check if any feature sets were loaded 
    if not feature_sets:
        raise ValueError(f"No valid feature sets were loaded from {extracted_feature_dir}")
    
    return feature_sets