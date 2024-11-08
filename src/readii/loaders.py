"""DICOM, RTSTRUCT, and SEG loading functions.

This module provides functions to load and process DICOM series and RTSTRUCT
(Radiotherapy Structure Set) files using SimpleITK. It includes utilities to
read and convert DICOM images to SimpleITK images, as well as to extract
specific regions of interest (ROIs) from RTSTRUCT files. The functions can
handle various DICOM modalities, making it easier to work with medical
imaging data.
"""

from pathlib import Path
from typing import Dict, Optional

import pydicom
import SimpleITK as sitk
from imgtools import io
from imgtools.ops import StructureSetToSegmentation

from readii.utils.logging_config import logger

def loadDicomSITK(imgDirPath: str | Path) -> sitk.Image:
    """Read a DICOM series as a SimpleITK Image.

    Parameters
    ----------
        imgDirPath (Union[str, Path]): The path to the directory containing the DICOM series to
        load. It can be either a string or a Path object.

    Returns
    -------
        sitk.Image: The loaded image.
    """
    imgDirPath = Path(imgDirPath)
    try:
        logger.debug(f"Loading DICOM series from directory: {imgDirPath}")
        reader = sitk.ImageSeriesReader()
        dicomNames = reader.GetGDCMSeriesFileNames(str(imgDirPath))
        if not dicomNames:
            raise ValueError(f"No DICOM files found in directory: {imgDirPath}")
        reader.SetFileNames(dicomNames)
        return reader.Execute()
    except Exception as e:
        logger.exception("Error loading DICOM series: %s", e)
        raise


def loadRTSTRUCTSITK(
    rtstructPath: str | Path,
    baseImageDirPath: str | Path,
    roiNames: Optional[str] = None,
) -> Dict[str, sitk.Image]:
    """Load RTSTRUCT into SimpleITK Image.

    Parameters
    ----------
    rtstructPath : str or Path
        Path to the DICOM file containing the RTSTRUCT.
    baseImageDirPath : str or Path
        Path to the directory containing the DICOMs for the original image the segmentation
        was created from (e.g., CT). This is required to load the RTSTRUCT.
    roiNames : str, optional
        Identifier for which region(s) of interest to load from the total segmentation file.

    Returns
    -------
    dict
        A dictionary of mask ROIs from the loaded RTSTRUCT image as
        SimpleITK image objects.
    """
    # Convert to Path if passed as a string
    rtstructPath = Path(rtstructPath)
    baseImageDirPath = Path(baseImageDirPath)

    logger.debug("Loading RTSTRUCT")
    baseImage: io.Scan = io.read_dicom_scan(baseImageDirPath.resolve())
    segImage: io.StructureSet = io.read_dicom_rtstruct(rtstructPath.resolve())

    try:
        logger.debug(
            "Creating StructureSetToSegmentation object",
            roiNames=roiNames,
            continuous=True,
        )
        makeMask = StructureSetToSegmentation(roi_names=roiNames, continuous=True)
        # Get the individual ROI masks
        segMasks = makeMask(
            segImage,
            baseImage.image,
            existing_roi_indices={"background": 0},
            ignore_missing_regex=False,
        )
    except IndexError:
        logger.exception("Error making mask:")
        raise
    except ValueError as ve:
        logger.exception(f"Error making mask: {ve}")
        raise

    logger.debug("Finished making mask", seg_roi_names=segMasks.raw_roi_names)

    # Get list of ROIs present in this rtstruct
    loadedROINames = segMasks.raw_roi_names
    # Initialize dictionary to store ROI names and images
    roiStructs = {}
    # Get each roi and its label and store in dictionary
    for name in loadedROINames:
        # Get the mask for this ROI
        roiMask = segMasks.get_label(name=name)
        # Store the ROI name and image
        roiStructs[name] = roiMask

    return roiStructs


def loadSegmentation(
    segImagePath: str | Path,
    modality: str,
    baseImageDirPath: Optional[str | Path] = None,
    roiNames: Optional[str] = None,
) -> Dict[str, sitk.Image]:
    """Load a segmentation with the correct function.

    Parameters
    ----------
    segImagePath : str or Path
        Path to the segmentation file to load.
    modality : str
        Type of image that segImagePath points to load. If RTSTRUCT, must set baseImageDirPath.
    baseImageDirPath : str or Path, optional
        Path to the directory containing the DICOMs for the original image the segmentation
        was created from.
    roiNames : str, optional
        Identifier for which region(s) of interest to load from the total segmentation file.

    Returns
    -------
    dict
        A dictionary of each of the ROIs and their name in the segmentation
        image as sitk.Image objects.

    Examples
    --------
    >>> segImages = loadSegmentation(
    ...     segImagePath="/path/to/segmentation/1.dcm",
    ...     modality="RTSTRUCT",
    ...     baseImageDirPath="/path/to/CT",
    ...     roiNames="GTVp.*",
    ... )
    """
    if modality.upper() not in ["SEG", "RTSTRUCT"]:
        raise ValueError(
            f"Unsupported segmentation modality '{modality}'. Must be one of 'RTSTRUCT' or 'SEG'."
        )
    # Always convert paths to Path objects
    segImagePath = Path(segImagePath)
    if baseImageDirPath is not None:
        baseImageDirPath = Path(baseImageDirPath)

    if modality.upper() == "SEG":
        imgFolder = segImagePath.parent
        segHeader = pydicom.dcmread(segImagePath.resolve(), stop_before_pixels=True)
        roiName = segHeader.SegmentSequence[0].SegmentLabel
        return {roiName: loadDicomSITK(imgFolder)}

    # modality is RTSTRUCT
    if baseImageDirPath is None:
        raise ValueError(
            "When loading RTSTRUCT, must pass baseImageDirPath since "
            "RTSTRUCT loader requires original image."
        )

    return loadRTSTRUCTSITK(
        segImagePath.resolve(),
        baseImageDirPath.resolve(),
        roiNames,
    )
