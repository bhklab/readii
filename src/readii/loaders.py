import os
import pydicom
import SimpleITK as sitk

from imgtools.ops import StructureSetToSegmentation
from imgtools.io import read_dicom_auto

from typing import Optional

from readii.utils import get_logger

# Create a global logger instance
logger = get_logger()

def loadDicomSITK(imgDirPath: str) -> sitk.Image:
    """Read DICOM series as SimpleITK Image.

    Parameters
    ----------
    img_path : str
        Path to directory containing the DICOM series to load.

    Returns
    -------
    sitk.Image
        The loaded image.
    """
    # Set up the reader for the DICOM series
    logger.debug(f"Loading DICOM series from directory: {imgDirPath}")
    reader = sitk.ImageSeriesReader()
    dicomNames = reader.GetGDCMSeriesFileNames(imgDirPath)
    reader.SetFileNames(dicomNames)
    return reader.Execute()


def loadRTSTRUCTSITK(
    rtstructPath: str, baseImageDirPath: str, roiNames: Optional[str] = None
) -> dict:
    """Load RTSTRUCT into SimpleITK Image.

    Parameters
    ----------
    rtstructPath : str
        Path to the DICOM file containing the RTSTRUCT
    baseImageDirPath : str
        Path to the directory containing the DICOMS for the original image the segmentation
        was created from (e.g. CT). This is required to load the RTSTRUCT.
    roiNames : str
        Identifier for which region(s) of interest to load from the total segmentation file

    Returns
    -------
    dict
        A dictionary of mask ROIs from the loaded RTSTRUCT image as a SimpleITK image objects.
        The segmentation label is set to 1.
    """
    # Set up segmentation loader
    logger.debug(f"Making mask using ROI names: {roiNames}")
    makeMask = StructureSetToSegmentation(roi_names=roiNames)

    # Read in the base image (CT) and segmentation DICOMs into SITK Images
    logger.debug(f"Loading RTSTRUCT from directory: {rtstructPath}")
    baseImage = read_dicom_auto(baseImageDirPath)
    segImage = read_dicom_auto(rtstructPath)

    try:
        # Get the individual ROI masks
        segMasks = makeMask(
            segImage,
            baseImage.image,
            existing_roi_indices={"background": 0},
            ignore_missing_regex=False,
        )
    except ValueError:
        return {}

    # Get list of ROIs present in this rtstruct
    loadedROINames = segMasks.raw_roi_names
    # Initialize dictionary to store ROI names and images
    roiStructs = {}
    # Get each roi and its label and store in dictionary
    for roi in loadedROINames:
        # Get the mask for this ROI
        roiMask = segMasks.get_label(name=roi)
        # Store the ROI name and image
        roiStructs[roi] = roiMask

    return roiStructs


def loadSegmentation(
    segImagePath: str,
    modality: str,
    baseImageDirPath: Optional[str] = None,
    roiNames: Optional[str] = None,
) -> dict:
    """Function to load a segmentation with the correct function.

    Parameters
    ----------
    segImagePath : str
        Path to the segmentation file to load
    modality : str
        Type of image that imgPath points to to load. If RTSTRUCT, must set baseImageDirPath
    baseImageDirPath : str
        Path to the directory containing the DICOMS for the original image the segmentation
        was created from.
    roiNames : str
        Identifier for which region(s) of interest to load from the total segmentation file

    Returns
    -------
    dict
        A dictionary of each of the ROIs and their name in the segmentation image as sitk.Image objects.

    Examples
    --------
    >>> segImages = loadSegmentation("/path/to/segmentation/1.dcm", 'RTSTRUCT', '/path/to/CT', 'GTVp.*')
    """

    if modality in ["SEG", "seg"]:
        # Loading SEG requires directory containing file, not the actual file path
        imgFolder, _ = os.path.split(segImagePath)
        segHeader = pydicom.dcmread(segImagePath, stop_before_pixels=True)
        roiName = segHeader.SegmentSequence[0].SegmentLabel
        return {roiName: loadDicomSITK(imgFolder)}

    elif modality in ["RTSTRUCT", "rtstruct"]:
        if baseImageDirPath == None:
            raise ValueError(
                "Missing path to original image segmentation was taken from. RTSTRUCT loader requires original image."
            )
        else:
            return loadRTSTRUCTSITK(segImagePath, baseImageDirPath, roiNames)

    else:
        raise ValueError(
            "This segmentation modality is not supported. Must be one of RTSTRUCT or SEG"
        )
