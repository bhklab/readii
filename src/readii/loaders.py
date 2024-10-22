"""DICOM and RTSTRUCT Loading Utilities for Medical Imaging.

This module provides functions to load and process DICOM series and RTSTRUCT
(Radiotherapy Structure Set) files using SimpleITK. It includes utilities to
read and convert DICOM images to SimpleITK images, as well as to extract
specific regions of interest (ROIs) from RTSTRUCT files. The functions can
handle various DICOM modalities, making it easier to work with medical
imaging data.
"""

import os
from pathlib import Path
from typing import Optional

import imgtools.io as io
import pydicom
import SimpleITK as sitk
from imgtools.ops import StructureSetToSegmentation

from readii.utils import get_logger

# Create a global logger instance
logger = get_logger()


def loadDicomSITK(imgDirPath: str) -> sitk.Image:
    """Read DICOM series as SimpleITK Image.

    Parameters
    ----------
    imgDirPath : str
        Path to directory containing the DICOM series to load.

    Returns:
    -------
    sitk.Image
        The loaded image.

    """
    # Set up the reader for the DICOM series
    logger.debug(f'Loading DICOM series from directory: {imgDirPath}')
    reader = sitk.ImageSeriesReader()
    dicomNames = reader.GetGDCMSeriesFileNames(imgDirPath)
    reader.SetFileNames(dicomNames)
    return reader.Execute()


def loadRTSTRUCTSITK(
    rtstructPath: str, baseImageDirPath: str, roiNames: Optional[str] = None
) -> dict[str, sitk.Image]:
    """Load RTSTRUCT into SimpleITK Image.

    Parameters
    ----------
    rtstructPath : str
        Path to the DICOM file containing the RTSTRUCT
    baseImageDirPath : str
        Path to the directory containing the DICOMS for the original image the
        segmentation was created from (e.g. CT). This is required to load the
        RTSTRUCT.
    roiNames : str
        Identifier for which region(s) of interest to load from the total
        segmentation file

    Returns:
    -------
    dict
        A dictionary of mask ROIs from the loaded RTSTRUCT image as a
        SimpleITK image objects.The segmentation label is set to 1.

    """
    if not Path(rtstructPath).is_file():
        raise FileNotFoundError(
            f'RTSTRUCT file {rtstructPath} does not exist or is not a file.'
        )
    if not Path(baseImageDirPath).is_dir():
        raise FileNotFoundError(
            f'Base image directory {baseImageDirPath} '
            'does not exist or is not a directory.'
        )

    # Read in the base image (CT) and segmentation DICOMs into SITK Images
    logger.debug(f'Loading RTSTRUCT from directory: {rtstructPath}')

    baseImage: io.Scan = io.read_dicom_scan(baseImageDirPath)
    segImage: io.StructureSet = io.read_dicom_rtstruct(rtstructPath)

    # Set up segmentation loader
    logger.debug(f'Making mask using ROI names: {roiNames}')
    makeMask = StructureSetToSegmentation(roi_names=roiNames)

    try:
        # Get the individual ROI masks
        segMasks: io.Segmentation = makeMask(
            segImage,
            baseImage.image,
            existing_roi_indices={'background': 0},
            ignore_missing_regex=False,
        )
    except ValueError as e:
        logger.error(
            'Error loading segmentation masks from RTSTRUCT',
            exc_info=True,
        )
        raise e

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
) -> dict[str, sitk.Image]:
    """Load a segmentation with the correct function.

    Parameters
    ----------
    segImagePath : str
        Path to the segmentation file to load
    modality : str
        Type of image that imgPath points to to load. If RTSTRUCT, must
        set baseImageDirPath
    baseImageDirPath : str
        Path to the directory containing the DICOMS for the original image
        the segmentation was created from.
    roiNames : str
        Identifier for which region(s) of interest to load from the total
        segmentation file

    Returns:
    -------
    dict
        A dictionary of each of the ROIs and their name in the segmentation
        image as sitk.Image objects.

    Examples:
    --------
    >>> segImages = loadSegmentation(
    ...     '/path/to/segmentation/1.dcm',
    ...     'RTSTRUCT',
    ...     '/path/to/CT',
    ...     'GTVp.*',
    ... )

    """
    assert modality.upper() in ['RTSTRUCT', 'SEG']

    # if modality in ['SEG', 'seg']:
    if modality.upper() == 'SEG':
        # Loading SEG requires directory containing file, not actual file path
        imgFolder, _ = os.path.split(segImagePath)
        segHeader = pydicom.dcmread(segImagePath, stop_before_pixels=True)
        roiName = segHeader.SegmentSequence[0].SegmentLabel
        return {roiName: loadDicomSITK(imgFolder)}

    # else, modality.upper() is 'RTSTRUCT'
    if baseImageDirPath is None:
        raise ValueError(
            'Missing path to original image segmentation was taken from. '
            'RTSTRUCT loader requires original image.'
        )
    else:
        return loadRTSTRUCTSITK(segImagePath, baseImageDirPath, roiNames)
