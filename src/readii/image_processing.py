from dicom_parser import Series
import matplotlib.pyplot as plt
import numpy as np
import pydicom
from radiomics import imageoperations
import SimpleITK as sitk

from typing import Optional

from readii.loaders import (
    loadDicomSITK,
    loadRTSTRUCTSITK,
    loadSegmentation,
)


def flattenImage(image: sitk.Image) -> sitk.Image:
    """Remove axes of image with size one. (ex. shape is [1, 100, 256, 256])

    Parameters
    ----------
    image : sitk.Image
        Image to remove axes with size one.

    Returns
    -------
    sitk.Image
        image with axes of length one removed.
    """
    imageArr = sitk.GetArrayFromImage(image)

    imageArr = np.squeeze(imageArr)

    return sitk.GetImageFromArray(imageArr)


def alignImages(originImage: sitk.Image, movingImage: sitk.Image) -> sitk.Image:
    """Align movingImage to the originImage so origin and direction match

    Parameters
    ----------
    originImage : sitk.Image
        Image to use to set direction and origin for the movingImage

    movingImage : sitk.Image
        Image to align to originImage

    Returns
    -------
    sitk.Image
        movingImage now aligned to originImage
    """
    movingImage.SetDirection(originImage.GetDirection())
    movingImage.SetOrigin(originImage.GetOrigin())
    movingImage.SetSpacing(originImage.GetSpacing())

    return movingImage


def padSegToMatchCT(
    ctDirPath: str,
    segImagePath: Optional[str] = None,
    ctImage: Optional[sitk.Image] = None,
    alignedSegImage: Optional[sitk.Image] = None,
) -> sitk.Image:
    """Function to take a segmentation that doesn't have the same slice count as the CT image, maps it to the corresponding
        CT slices, and pads it with slices containing 0s so it maps properly onto the original image.

    Parameters
    ----------
    ctDirPath : str
        Path to DICOM series folder containing all CT image files. Must be a directory.

    segImagePath : str
        Path to the DICOM SEG file that corresponds with CT in ctDirPath that has incorrect slice count.

    ctImage : sitk.Image
        Optional argument, base image to align the padded segmentation image to. If None is passed, will be loaded in from ctFolderPath.

    alignedSegImage : sitk.Image
        Optional argument, if image has already been loaded it can be passed in to be adjusted.
        Assumes that flattenImage and alignImages has already been run.
        If not passed, will use segFilePath to load the image.

    Returns
    -------
    sitk.Image
    Padded segmentation with the same dimensions as the CT.

    Examples
    --------
    >>> paddedSeg = padSegToMatchCT("/path/to/CT", "/path/to/segmentation/1.dcm")

    >>> lungCT = loadDicomSITK("/path/to/CT")
    >>> tumourSeg = loadSegmentation("/path/to/segmentation/1.dcm", 'SEG')
    >>> paddedSeg = padSegToMatchCT("/path/to/CT", ctImage = lungCT, alignedSegImage = tumourSeg)
    """

    # Load the CT image to align the segmentation to if not passed as argument
    if ctImage is None:
        ctImage = loadDicomSITK(ctDirPath)

    # Load in the segmentation image if not passed as argument
    if alignedSegImage is None:
        if segImagePath is None:
            raise ValueError(
                "Must pass either a loaded and aligned segmentation or the path to load the segmentation from."
            )
        else:
            segImage = loadSegmentation(segImagePath, modality="SEG")
            # Segmentation contains extra axis, flatten to 3D by removing it
            segImage = flattenImage(segImage)
            # Segmentation has different origin, align it to the CT for proper feature extraction
            alignedSegImage = alignImages(ctImage, segImage)

    # Load in header information for the CT and SEG files
    ctSeries = Series(ctDirPath)
    segWithHeader = pydicom.dcmread(segImagePath, stop_before_pixels=True)

    # Get the first and last reference ID for the slices of the CT that are in the SEG file
    lastSliceRef = (
        segWithHeader.ReferencedSeriesSequence[0]
        .ReferencedInstanceSequence[0]
        .ReferencedSOPInstanceUID
    )
    firstSliceRef = (
        segWithHeader.ReferencedSeriesSequence[0]
        .ReferencedInstanceSequence[-1]
        .ReferencedSOPInstanceUID
    )

    # Get the index of the reference IDs in the CT image
    firstSliceIdx = ctSeries["SOPInstanceUID"].index(firstSliceRef)
    lastSliceIdx = ctSeries["SOPInstanceUID"].index(lastSliceRef)

    # Convert the segmentation image to an array and pad with 0s so segmentation mask is in the correct indices
    arrSeg = sitk.GetArrayFromImage(alignedSegImage)
    padArrSeg = np.pad(
        arrSeg,
        (
            (
                (firstSliceIdx, (ctSeries.data.shape[-1] - lastSliceIdx - 1)),
                (0, 0),
                (0, 0),
            )
        ),
        "constant",
        constant_values=(0),
    )

    # Convert back to Image object
    paddedSegImage = sitk.GetImageFromArray(padArrSeg)
    paddedSegImage = alignImages(ctImage, paddedSegImage)

    return paddedSegImage


def displayImageSlice(
    image, 
    sliceIdx, 
    cmap=plt.cm.Greys_r, 
    dispMin=None, 
    dispMax=None
) -> None:
    """Function to display a 2D slice from a 3D image
        By default, displays slice in greyscale with min and max range set to min and max value in the slice.

    Parameters
    ----------
    image : sitk.Image or nd.array
        The complete image you'd like to display a slice of. If an array, must have slices as first dimension
    sliceIdx : int
        Slice index from image to display
    cmap : matplotlib.colormap
        Color map to use for plot, see https://matplotlib.org/stable/tutorials/colors/colormaps.html for options
    dispMin : int
        Value to use as min for cmap in display
    dispMax : int
        Value to use as max for cmap in display
    """
    # If image is a simple ITK image, convert to array for display
    if type(image) == sitk.Image:
        image = sitk.GetArrayFromImage(image)

    # Get min and max value from image to define range in display
    if dispMin == None:
        dispMin = image.min()
    if dispMax == None:
        dispMax = image.max()

    # Display the slice of the image
    plt.imshow(image[sliceIdx, :, :], cmap=cmap, vmin=dispMin, vmax=dispMax)
    plt.axis("off")


def displayCTSegOverlay(
    ctImage,
    segImage,
    sliceIdx=-1,
    cmapCT=plt.cm.Greys_r,
    cmapSeg=plt.cm.brg,
    alpha=0.3,
    crop=False,
) -> None:
    """Function to display a 2D slice from a CT with the ROI from a segmentation image overlaid in green
    Parameters
    ----------
    ctImage : sitk.Image or nd.array
        CT image to display a slice of. If an array, must have slices as first dimension.
    segImage : sitk.Image or nd.array
        Segmentation image containing a ROI to overlay with CT. Must be aligned to CT. If an array, must have slices as first dimension
        and have background labeled as 0s.
    sliceIdx : int
        Slice index from image to display. If not provided, will get center slice of ROI to plot.
    cmapCT : matplotlib.colormap
        Color map to use for CT plot, see https://matplotlib.org/stable/tutorials/colors/colormaps.html for options. Is greyscale by default.
    cmapSeg: matplotlib.colormap
        Color map to use for ROI plot, see https://matplotlib.org/stable/tutorials/colors/colormaps.html for options. Is green by default.
    alpha : float
        Value between 0 and 1 indicating transparency of ROI overtop of CT. Default is 0.3
    crop : bool
        Whether to crop the output image to the ROI in the segmentation.
    """
    # If crop indicated, crop the CT and segmentation to just around the ROI
    if crop:
        ctImage, segImage = getCroppedImages(ctImage, segImage)

    # If slice index is not provided, get the center slice for the ROI in segImage
    if sliceIdx == -1:
        sliceIdx, _, _ = getROICenterCoords(segImage)

    # If image is a simple ITK image, convert to array for display
    if type(ctImage) == sitk.Image:
        ctImage = sitk.GetArrayFromImage(ctImage)
    # If segmentation is a simple ITK image, convert to array for display
    if type(segImage) == sitk.Image:
        segImage = sitk.GetArrayFromImage(segImage)

    # Make mask of ROI to ignore background in overlaid plot
    maskSeg = np.ma.masked_where(segImage == 0, segImage)

    # Plot slice of CT
    plt.imshow(
        ctImage[sliceIdx, :, :], cmap=cmapCT, vmin=ctImage.min(), vmax=ctImage.max()
    )
    # Plot mask of ROI overtop
    plt.imshow(
        maskSeg[sliceIdx, :, :],
        cmap=cmapSeg,
        vmin=segImage.min(),
        vmax=segImage.max(),
        alpha=alpha,
    )
    plt.axis("off")


def getROICenterCoords(segImage: sitk.Image):
    """A function to find the slice number and coordinates for the center of an ROI in a loaded RTSTRUCT or SEG file.

    Parameters
    ----------
    segImage
        sitk.Image, a loaded segmentation image, should be binary with segmentation voxels as a non-zero value

    Returns
    -------
    centerSliceIdx : int
        Index of the centermost slice of the ROI in the image
    centerColumnPixelIdx : int
        Column index of the centermost point in the ROI in the center slice.
    centerRowPixelIdx : int
        Row index of the centermost point in the ROI in the center slice.
    """
    # Convert segmentation image to a numpy array
    arrSeg = sitk.GetArrayFromImage(segImage)

    nonZeroIndices = np.nonzero(arrSeg)
    nzSliceIndices = nonZeroIndices[0]
    nzColumnIndices = nonZeroIndices[1]
    nzRowIndices = nonZeroIndices[2]

    centerSliceIdx = nzSliceIndices[int(len(nzSliceIndices) / 2)]
    centerColumnPixelIdx = nzColumnIndices[int(len(nzColumnIndices) / 2)]
    centerRowPixelIdx = nzRowIndices[int(len(nzRowIndices) / 2)]

    return centerSliceIdx, centerColumnPixelIdx, centerRowPixelIdx


def getROIVoxelLabel(segImage: sitk.Image):
    """A function to find the non-zero value that identifies segmentation voxels in a loaded RTSTRUCT or SEG file.

    Parameters
    ----------
    segImage
        sitk.Image, a loaded segmentation image, should be binary with segmentation voxels as a non-zero value

    Returns
    -------
    labelValue
        int, the label value for the segmentation voxels
    """

    # Convert segmentation image to a numpy array
    arrSeg = sitk.GetArrayFromImage(segImage)
    # Get all values that aren't 0 - these will identify the ROI
    roiVoxels = arrSeg[arrSeg != 0]
    # Confirm that all of these are the same value
    if np.all(roiVoxels == roiVoxels[0]):
        labelValue = roiVoxels[0]
        return int(labelValue)
    else:
        raise ValueError(
            "Multiple label values present in this segmentation. Must all be the same."
        )


def getCroppedImages(ctImage, segImage, segmentationLabel=None):
    """A function to crop a CT and segmentation to close to the ROI within the segmentation.

    Parameters
    ----------
    ctImage : sitk.Image
        CT image to crop.
    segImage : sitk.Image
        Segmentation image containing a ROI to overlay with CT. Must be aligned to CT.
    segmentationLabel : int
        Value of pixels within the ROI in the segImage. If not passed, will use getROIVoxelLabel to find it.

    Returns
    -------
    croppedCT : sitk.Image
        CT cropped to bounding box around ROI
    croppedROI : sitk.Image
        Segmentation cropped to bounding box around ROI.
    """
    if segmentationLabel == None:
        segmentationLabel = getROIVoxelLabel(segImage)

    # Check that CT and segmentation correspond, segmentationLabel is present, and dimensions match
    segBoundingBox, correctedROIImage = imageoperations.checkMask(
        ctImage, segImage, label=segmentationLabel
    )
    # Update the ROI image if a correction was generated by checkMask
    if correctedROIImage is not None:
        segImage = correctedROIImage

    # Crop the image and mask to a bounding box around the mask to reduce volume size to process
    croppedCT, croppedROI = imageoperations.cropToTumorMask(
        ctImage, segImage, segBoundingBox
    )

    return croppedCT, croppedROI
