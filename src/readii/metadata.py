import os
import pandas as pd
from typing import Optional, Literal
from readii.utils import get_logger

logger = get_logger()

def createImageMetadataFile(outputDir, parentDirPath, datasetName, segType, imageFileListPath, update = False):
    imageMetadataPath = os.path.join(outputDir, "ct_to_seg_match_list_" + datasetName + ".csv")
    if os.path.exists(imageMetadataPath) and not update:
        logger.info(f"Image metadata file {imageMetadataPath} already exists & update flag is {update}.")
        return imageMetadataPath
    elif update:
        logger.info(f"{update=}, Image metadata file {imageMetadataPath} will be overwritten.")
    else:
        logger.info(f"Image metadata file {imageMetadataPath} not found.. creating...")
    
    if segType == "RTSTRUCT":
        imageFileEdgesPath = os.path.join(parentDirPath + "/.imgtools/imgtools_" + datasetName + "_edges.csv")
        getCTWithSegmentation(imgFileEdgesPath = imageFileEdgesPath,
                                segType = segType,
                                outputFilePath = imageMetadataPath)
    elif segType == "SEG":
        matchCTtoSegmentation(imgFileListPath = imageFileListPath,
                                segType = segType,
                                outputFilePath = imageMetadataPath)
    else:
        logger.info(f"Expecting either RTSTRUCT or SEG segmentation type. Found {segType}.")
        raise ValueError("Incorrect segmentation type or segmentation type is missing from med-imagetools output. Must be RTSTRUCT or SEG.")
    return imageMetadataPath

def saveDataframeCSV(
    dataframe: pd.DataFrame, 
    outputFilePath: str
) -> None:
    """Function to save a pandas Dataframe as a csv file with the index removed.
            Checks if the path in the outputFilePath exists and will create any missing directories.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Pandas dataframe to save out as a csv
    outputFilePath : str
        Full file path to save the dataframe out to.
            
    Raises
    ------
    ValueError
        If the outputFilePath does not end in .csv, if the dataframe is not a pandas DataFrame, 
        or if an error occurs while saving the dataframe.
    """
    
    if not outputFilePath.endswith(".csv"):
        raise ValueError(
            "This function saves .csv files, so outputFilePath must end in .csv"
        )

    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("Function expects a pandas DataFrame to save out.")

    # Make directory if it doesn't exist, but don't fail if it already exists
    os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)

    try:
        # Save out DataFrame
        dataframe.to_csv(outputFilePath, index=False)
    except Exception as e:
        error_msg = f"An error occurred while saving the DataFrame: {str(e)}"
        raise ValueError(error_msg) from e
    else:
        return


def matchCTtoSegmentation(
    imgFileListPath: str, 
    segType: str, 
    outputFilePath: Optional[str] = None,
) -> pd.DataFrame:
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
    outputDirPath : str
        Optional file path to save the dataframe to as a csv.

    Returns
    -------
    pd.Dataframe
        Dataframe containing the CT and corresponding segmentation data for each patient
    
    Raises
    ------
    ValueError
        If the segmentation file type is not RTSTRUCT or SEG, or if the imgFileListPath does not end in .csv

    Note: All subseries of CT will be kept in the dataframe in this function
    """
    # Check that segmentation file type is acceptable
    if segType not in ["RTSTRUCT", "SEG"]:
        raise ValueError("Incorrect segmentation file type. Must be RTSTRUCT or SEG.")

    # Check that imgFileListPath is a csv file to properly be loaded in
    if not imgFileListPath.endswith(".csv"):
        raise ValueError(
            "This function expects to load in a .csv file, so imgFileListPath must end in .csv"
        )

    if not os.path.exists(imgFileListPath):
        logger.error(f"Image file list {imgFileListPath} not found.")
        raise FileNotFoundError("Image file list not found.")
    
    # Load in complete list of patient image directories of all modalities (output from med-imagetools crawl)
    fullDicomList: pd.DataFrame = pd.read_csv(imgFileListPath, index_col=0)

    # Extract all CT rows
    allCTRows: pd.DataFrame = fullDicomList.loc[fullDicomList["modality"] == "CT"]

    # Extract all SEG rows
    allSegRows: pd.DataFrame = fullDicomList.loc[fullDicomList["modality"] == segType]

    # Merge the CT and segmentation dataframes based on the CT ID (referenced in the segmentation rows)
    # Uses only segmentation keys, so no extra CTs are kept
    # If multiple CTs have the same ID, they are both included in this table
    samplesWSeg: pd.DataFrame = allCTRows.merge(
        allSegRows,
        how="inner",
        left_on=["series", "patient_ID"],
        right_on=["reference_ct", "patient_ID"],
        suffixes=("_CT", "_seg"),
    )

    # Sort dataframe by ascending patient ID value
    samplesWSeg.sort_values(by="patient_ID", inplace=True)

    # Save out the combined list
    if outputFilePath != None:
        saveDataframeCSV(samplesWSeg, outputFilePath)

    return samplesWSeg


def getCTWithSegmentation(imgFileEdgesPath: str, 
                          segType: str = "RTSTRUCT",
                          outputFilePath: Optional[str] = None,
) -> pd.DataFrame:
    """From full list of image files edges from med-imagetools, get the list of CTs with segmentation.
    These are marked as edge type 2 in the edges file.
    Note: This function can only handle RTSTRUCT segmentations as this is what med-imagetools catches at this point.

    Parameters
    ----------
    imgFileEdgesPath : str
        Path to csv containing list of image directories/paths in the dataset with the edge types.
        Expecting output from med-imagetools autopipeline .imgtools_[dataset]_edges
    segType : str
        Type of file segmentation is in. Must be RTSTRUCT.
    outputFilePath : Optional[str]
        Optional file path to save the dataframe to as a csv.

    Returns
    -------
    pd.Dataframe
        Dataframe containing the CT and corresponding segmentation data for each patient
    
    Raises
    ------
    ValueError
        If the segmentation file type is not RTSTRUCT, or if the imgFileEdgesPath does not end in .csv
    """

    # Check that segmentation file type is acceptable
    if segType != "RTSTRUCT":
        raise ValueError("Incorrect segmentation file type. Must be RTSTRUCT. For SEG, use matchCTtoSegmentation.")

    # Check that imgFileListPath is a csv file to properly be loaded in
    if not imgFileEdgesPath.endswith(".csv"):
        raise ValueError(
            "This function expects to load in a .csv file, so imgFileEdgesPath must end in .csv"
        )
    
    # Load in complete list of patient image directories of all modalities and edge types(output from med-imagetools crawl)
    fullDicomEdgeList: pd.DataFrame = pd.read_csv(imgFileEdgesPath)

    # Get just the CTs with segmentations, marked as edge type 2 in the edges file
    samplesWSeg: pd.DataFrame = fullDicomEdgeList.loc[fullDicomEdgeList["edge_type"] == 2]

    # Replace the _x and _y suffixes in the column names with _CT and _seg to match matchCTtoSegmentation
    samplesWSeg.columns = samplesWSeg.columns.str.replace("_x", "_CT", regex=True)
    samplesWSeg.columns = samplesWSeg.columns.str.replace("_y", "_seg", regex=True)

    # Remove the _CT suffix from the patient_ID column to match matchCTtoSegmentation
    samplesWSeg.rename(columns={"patient_ID_CT": "patient_ID"}, inplace=True)

    sortedSamplesWSeg = samplesWSeg.sort_values(by="patient_ID")

    # Save out the combined list
    if outputFilePath != None:
        saveDataframeCSV(sortedSamplesWSeg, outputFilePath)

    return sortedSamplesWSeg


def getSegmentationType(
    imgFileListPath: str
) -> Literal['RTSTRUCT', 'SEG']:
    """Find the segmentation type from the full list of image files.

    Parameters
    ----------
    imgFileListPath : str
        Path to csv containing list of image directories/paths in the dataset.
        Expecting output from med-imagetools autopipeline .imgtools_[dataset]

    Returns
    -------
    str
        Segmentation type (RTSTRUCT or SEG)
        
    Raises
    ------
    ValueError
        If the imgFileListPath does not end in .csv
    RuntimeError
        If no suitable segmentation type is found in the dataset
    """
    # Check that imgFileListPath is a csv file to properly be loaded in
    if not imgFileListPath.endswith(".csv"):
        raise ValueError(
            "This function expects to load in a .csv file, so imgFileListPath must end in .csv"
        )

    # Load in complete list of patient image directories of all modalities (output from med-imagetools crawl)
    fullDicomList: pd.DataFrame = pd.read_csv(imgFileListPath, index_col=0)

    # Get list of unique modalities
    modalities = list(fullDicomList["modality"].unique())
    logger.debug(f"Modalities found: {modalities}")
    
    if "RTSTRUCT" in modalities:
        segType = "RTSTRUCT"
    elif "SEG" in modalities:
        segType = "SEG"
    else:
        raise RuntimeError(
            "No suitable segmentation type found. READII can only use RTSTRUCTs and DICOM-SEG segmentations."
        )

    return segType
