import os
import pandas as pd 

def saveDataframeCSV(dataframe: pd.DataFrame,
                     outputFilePath: str):
    """ Function to save a pandas Dataframe as a csv file with the index removed.
            Checks if the path in the outputFilePath exists and will create any missing directories.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Pandas dataframe to save out as a csv
    outputFilePath : str
        Full file path to save the dataframe out to.
    """
    if not outputFilePath.endswith('.csv'):
        raise ValueError("This function saves .csv files, so outputFilePath must end in .csv")

    # Make directory if it doesn't exist
    if not os.path.exists(os.path.dirname(outputFilePath)):
        os.makedirs(os.path.dirname(outputFilePath))

    # Save out feature set
    dataframe.to_csv(outputFilePath, index=False)

    return


def matchCTtoSegmentation(imgFileListPath: str,
                          segType: str,
                          outputFilePath: str = None):
    """From full list of image files, extract CT and corresponding segmentation files and create new table.
    One row of the table contains both the CT and segmentation data for one patient.
    This function currently assumes there is one segmentation for each patient.

    Parameters
    ----------
    imgFileListPath : str
        Path to csv containing list of image directories/paths in the dataset. 
        Expecting output from med-imagetools autopipeline .imgtools_[dataset]
    segType : str
        Type of file segmentation is in. Can be SEG or RTSTRUCT.
    outputFilePath : str
        Optional file path to save the dataframe to as a csv.
    
    Returns
    -------
    pd.Dataframe
        Dataframe containing the CT and corresponding segmentation data for each patient

    Note: All subseries of CT will be kept in the dataframe in this function
    """
    # Check that segmentation file type is acceptable
    if segType != "RTSTRUCT" and segType != "SEG":
        raise ValueError("Incorrect segmentation file type. Must be RTSTRUCT or SEG.")

    # Load in complete list of patient image directories of all modalities (output from med-imagetools crawl)
    fullDicomList = pd.read_csv(imgFileListPath, index_col=0)

    # Extract all CT rows
    allCTRows = fullDicomList.loc[fullDicomList['modality'] == "CT"]

    # Extract all SEG rows
    allSegRows = fullDicomList.loc[fullDicomList['modality'] == segType]

    # Merge the CT and segmentation dataframes based on the CT ID (referenced in the segmentation rows)
    # Uses only segmentation keys, so no extra CTs are kept
    # If multiple CTs have the same ID, they are both included in this table
    samplesWSeg = allCTRows.merge(allSegRows, how='right', 
                                  left_on=['series', 'patient_ID'], 
                                  right_on=['reference_ct', 'patient_ID'], 
                                  suffixes=('_CT','_seg'))

    # Sort dataframe by ascending patient ID value
    samplesWSeg.sort_values(by='patient_ID', inplace=True)

    # Save out the combined list
    if outputFilePath != None:
        saveDataframeCSV(samplesWSeg, outputFilePath)
    
    return samplesWSeg