from pathlib import Path
import pandas as pd
from typing import Optional, Literal, Union
from readii.utils.logging_config import logger


def createImageMetadataFile(
    outputDir: Union[str, Path],
    parentDirPath: Union[str, Path],
    datasetName: str,
    segType: str,
    imageFileListPath: Union[str, Path],
    update=False,
) -> Path:
    outputDir = Path(outputDir)
    parentDirPath = Path(parentDirPath)
    imageFileListPath = Path(imageFileListPath)

    imageMetadataPath = outputDir / f"ct_to_seg_match_list_{datasetName}.csv"
    if imageMetadataPath.exists() and not update:
        logger.info(
            f"Image metadata file {imageMetadataPath} already exists & update flag is {update}."
        )
        return imageMetadataPath
    elif update:
        logger.info(
            f"{update=}, Image metadata file {imageMetadataPath} will be overwritten."
        )
    else:
        logger.info(f"Image metadata file {imageMetadataPath} not found.. creating...")

    if segType == "RTSTRUCT":
        imageFileEdgesPath = (
            parentDirPath / f".imgtools/imgtools_{datasetName}_edges.csv"
        )
        getCTWithSegmentation(
            imgFileEdgesPath=imageFileEdgesPath,
            segType=segType,
            outputFilePath=imageMetadataPath,
        )
    elif segType == "SEG":
        matchCTtoSegmentation(
            imgFileListPath=imageFileListPath,
            segType=segType,
            outputFilePath=imageMetadataPath,
        )
    else:
        logger.info(
            f"Expecting either RTSTRUCT or SEG segmentation type. Found {segType}."
        )
        raise ValueError(
            "Incorrect segmentation type or segmentation type is missing from med-imagetools output. Must be RTSTRUCT or SEG."
        )
    return imageMetadataPath


def saveDataframeCSV(dataframe: pd.DataFrame, outputFilePath: Union[str, Path]) -> None:
    outputFilePath = Path(outputFilePath)

    if not outputFilePath.suffix == ".csv":
        raise ValueError(
            "This function saves .csv files, so outputFilePath must end in .csv"
        )

    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("Function expects a pandas DataFrame to save out.")

    outputFilePath.parent.mkdir(parents=True, exist_ok=True)

    try:
        dataframe.to_csv(outputFilePath, index=False)
    except Exception as e:
        error_msg = f"An error occurred while saving the DataFrame: {str(e)}"
        raise ValueError(error_msg) from e


def matchCTtoSegmentation(
    imgFileListPath: Union[str, Path],
    segType: str,
    outputFilePath: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    imgFileListPath = Path(imgFileListPath)
    if outputFilePath is not None:
        outputFilePath = Path(outputFilePath)

    if segType not in ["RTSTRUCT", "SEG"]:
        raise ValueError("Incorrect segmentation file type. Must be RTSTRUCT or SEG.")

    if not imgFileListPath.suffix == ".csv":
        raise ValueError(
            "This function expects to load in a .csv file, so imgFileListPath must end in .csv"
        )

    if not imgFileListPath.exists():
        logger.error(f"Image file list {imgFileListPath} not found.")
        raise FileNotFoundError("Image file list not found.")

    fullDicomList: pd.DataFrame = pd.read_csv(imgFileListPath, index_col=0)

    allCTRows: pd.DataFrame = fullDicomList.loc[fullDicomList["modality"] == "CT"]
    allSegRows: pd.DataFrame = fullDicomList.loc[fullDicomList["modality"] == segType]

    samplesWSeg: pd.DataFrame = allCTRows.merge(
        allSegRows,
        how="inner",
        left_on=["series", "patient_ID"],
        right_on=["reference_ct", "patient_ID"],
        suffixes=("_CT", "_seg"),
    )

    samplesWSeg.sort_values(by="patient_ID", inplace=True)

    if outputFilePath is not None:
        saveDataframeCSV(samplesWSeg, outputFilePath)

    return samplesWSeg


def getCTWithSegmentation(
    imgFileEdgesPath: Union[str, Path],
    segType: str = "RTSTRUCT",
    outputFilePath: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    imgFileEdgesPath = Path(imgFileEdgesPath)
    if outputFilePath is not None:
        outputFilePath = Path(outputFilePath)

    if segType != "RTSTRUCT":
        raise ValueError(
            "Incorrect segmentation file type. Must be RTSTRUCT. For SEG, use matchCTtoSegmentation."
        )

    if not imgFileEdgesPath.suffix == ".csv":
        raise ValueError(
            "This function expects to load in a .csv file, so imgFileEdgesPath must end in .csv"
        )

    try:
        fullDicomEdgeList: pd.DataFrame = pd.read_csv(imgFileEdgesPath)
    except Exception as e:
        logger.exception("Error reading image edges file: %s", e)
        raise

    samplesWSeg: pd.DataFrame = fullDicomEdgeList.loc[
        fullDicomEdgeList["edge_type"] == 2
    ]

    samplesWSeg.columns = samplesWSeg.columns.str.replace("_x", "_CT", regex=True)
    samplesWSeg.columns = samplesWSeg.columns.str.replace("_y", "_seg", regex=True)

    samplesWSeg.rename(columns={"patient_ID_CT": "patient_ID"}, inplace=True)

    sortedSamplesWSeg = samplesWSeg.sort_values(by="patient_ID")

    if outputFilePath is not None:
        saveDataframeCSV(sortedSamplesWSeg, outputFilePath)

    return sortedSamplesWSeg


def getSegmentationType(
    imgFileListPath: Union[str, Path],
) -> Literal["RTSTRUCT", "SEG"]:
    imgFileListPath = Path(imgFileListPath)

    if imgFileListPath.suffix != ".csv":
        raise ValueError("imgFileListPath must end in .csv")

    fullDicomList: pd.DataFrame = pd.read_csv(imgFileListPath, index_col=0)
    modalities = fullDicomList["modality"].unique()

    if len(modalities) == 0:
        logger.error("No modalities found in the image list.", imgFileListPath=imgFileListPath, df=fullDicomList.shape)
        raise ValueError("No modalities found in the image list.")

    logger.debug("Modalities found", modalities=modalities)

    if "RTSTRUCT" in modalities:
        return "RTSTRUCT"
    if "SEG" in modalities:
        return "SEG"

    raise RuntimeError("No suitable segmentation type found. Only 'RTSTRUCT' and 'SEG' are supported.")
