from dicom_parser import Series
import matplotlib.pyplot as plt
import numpy as np
import pydicom
import SimpleITK as sitk

from yarea.loaders import *

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


def padSegToMatchCT(ctDirPath:str,
                    segImagePath:str = None,
                    ctImage:sitk.Image = None,
                    alignedSegImage:sitk.Image = None) -> sitk.Image:
    ''' Function to take a segmentation that doesn't have the same slice count as the CT image, maps it to the corresponding
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
    '''

    # Load the CT image to align the segmentation to if not passed as argument
    if ctImage == None:
        ctImage = loadDicomSITK(ctFolderPath)

    # Load in the segmentation image if not passed as argument
    if alignedSegImage == None:
        if segImagePath == None:
            raise ValueError("Must pass either a loaded and aligned segmentation or the path to load the segmentation from.")
        else:
            segImage = loadSegmentation(segImagePath, modality="SEG")
            # Segmentation contains extra axis, flatten to 3D by removing it
            segImage = flattenImage(segImage)
            # Segmentation has different origin, align it to the CT for proper feature extraction
            alignedSegImage = alignImages(ctImage, segImage)
    
    # Load in header information for the CT and SEG files
    ctSeries = Series(ctFolderPath)
    segWithHeader = pydicom.dcmread(segFilePath, stop_before_pixels=True)

    # Get the first and last reference ID for the slices of the CT that are in the SEG file
    lastSliceRef = segWithHeader.ReferencedSeriesSequence[0].ReferencedInstanceSequence[0].ReferencedSOPInstanceUID
    firstSliceRef = segWithHeader.ReferencedSeriesSequence[0].ReferencedInstanceSequence[-1].ReferencedSOPInstanceUID

    # Get the index of the reference IDs in the CT image
    firstSliceIdx = ctSeries['SOPInstanceUID'].index(firstSliceRef)
    lastSliceIdx = ctSeries['SOPInstanceUID'].index(lastSliceRef)

    # Convert the segmentation image to an array and pad with 0s so segmentation mask is in the correct indices
    arrSeg = sitk.GetArrayFromImage(alignedSegImage)
    padArrSeg = np.pad(arrSeg, (((firstSliceIdx, (ctSeries.data.shape[-1]-lastSliceIdx-1)), (0,0), (0,0))), 'constant', constant_values=(0))

    # Convert back to Image object
    paddedSegImage = sitk.GetImageFromArray(padArrSeg)
    paddedSegImage = alignImages(ctImage, paddedSegImage)

    return paddedSegImage


def displayImageSlice(image, sliceIdx, cmap=plt.cm.Greys_r, dispMin = None, dispMax = None):
    ''' Function to display a 2D slice from a 3D image
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
    '''
    # If image is a simple ITK image, convert to array for display
    if type(image) == sitk.SimpleITK.Image:
        imgArray = sitk.GetArrayFromImage(image)
 
    # Get min and max value from image to define range in display
    if dispMin == None:
        dispMin = imgArray.min()
    if dispMax == None:
        dispMax = imgArray.max()

    # Display the slice of the image
    plt.imshow(imgArray[sliceIdx,:,:], cmap=cmap, vmin=dispMin, vmax=dispMax)
    plt.axis('off')

