import os
import pandas as pd 

from typing import Optional, Dict

from readii.io.loaders.general import loadFileToDataFrame


def loadFeatureFilesFromImageTypes(extracted_feature_dir:str,
                                   image_types:Optional[list]=['original'], 
                                   drop_labels:Optional[bool]=True, 
                                   labels_to_drop:Optional[list]=["patient_ID","survival_time_in_years","survival_event_binary"])->Dict[str,pd.DataFrame]:
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
    # Initialize dictionary to store the feature sets
    feature_sets = {}

    feature_file_list = os.listdir(extracted_feature_dir)

    # Loop through all the files in the directory
    for image_type in image_types:
        try:
            # Extract the image type feature csv file from the feature directory
            # This should return a list of length 1, so we can just take the first element
            image_type_feature_file = [file for file in feature_file_list if (image_type in file) and (file.endswith(".csv"))][0]
            # Remove the image type file from the list of feature files
            feature_file_list.remove(image_type_feature_file)
        except Exception as e:
            print(f"{e}\n No {image_type} feature csv files found in {extracted_feature_dir}")
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
        except Exception as e:
            print(f"{feature_file_path} does not have the labels {labels_to_drop} to drop.")
            # Skip to the next image type
            continue

        # Save the dataframe to the feature_sets dictionary
        feature_sets[image_type] = raw_feature_data
    
    return feature_sets