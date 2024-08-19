from venv import logger
import SimpleITK as sitk
from SimpleITK import Image
import numpy as np
import random

from readii.image_processing import alignImages, getROIVoxelLabel
from readii.utils import get_logger

from typing import Optional, Union
from numpy import ndarray

logger = get_logger()

def getArrayFromImageOrArray(imageOrArray: Union[Image, ndarray]) -> ndarray:
    """Function to convert a SimpleITK Image to a numpy array.
    
    Parameters
    ----------
    imageOrArray : sitk.Image | np.ndarray
        Image or array to convert to numpy array.

    Returns
    -------
    np.ndarray
        Numpy array version of the input image or array.
        
    Raises
    ------
    ValueError
        If the input is not a SimpleITK Image or numpy array.
    """
    assert isinstance(imageOrArray, Image) or isinstance(imageOrArray, ndarray), \
        "Input must be a SimpleITK Image or numpy array."

    if isinstance(imageOrArray, Image):
        return sitk.GetArrayFromImage(imageOrArray)
    elif isinstance(imageOrArray, ndarray):
        return imageOrArray    

def makeShuffleImage(
    baseImage: Union[Image, ndarray],
    randomSeed: Optional[int] = None,
) -> Union[Image, ndarray]:
    
    """Function to shuffle all pixel values in a sitk.Image or np.ndarray (developed for 3D, should work on 2D as well)

    Parameters
    ----------
    baseImage : sitk.Image | np.ndarray
        Image to shuffle the pixels in. Can be a sitk.Image or np.ndarray.
    randomSeed : int
        Value to initialize random number generator with. Set for reproducible results.
        
    Returns
    -------
    sitk.Image | np.ndarray
        Image with all pixel values randomly shuffled with same dimensions and object type as input image.
    """
    # # Check if baseImage is a sitk.Image or np.ndarray
    arrImage = getArrayFromImageOrArray(baseImage)

    # Get array dimensions to reshape back to
    imgDimensions = arrImage.shape

    # Flatten the 3D array to 1D so values can be shuffled
    flatArrImage = arrImage.flatten()

    # Set the random seed for np random generator
    randNumGen = np.random.default_rng(seed=randomSeed)

    # Shuffle the flat array
    randNumGen.shuffle(flatArrImage)

    # Reshape the array back into the original image dimensions
    shuffled3DArrImage = np.reshape(flatArrImage, imgDimensions)

    if type(baseImage) == sitk.Image:
        # Convert back to sitk Image
        shuffledImage = sitk.GetImageFromArray(shuffled3DArrImage)

        # Set the origin/direction/spacing from original image to shuffled image
        alignedShuffledImage = alignImages(baseImage, shuffledImage)

        # Return the shuffled image
        return alignedShuffledImage
    
    else:
        # Return the shuffled array
        return shuffled3DArrImage

def makeRandomImage(
    baseImage: Union[Image, ndarray],
    randomSeed: Optional[int] = None,
) -> Union[sitk.Image, np.ndarray]:
    """Function to generate random pixel values based on the range of values in a sitk.Image or np.ndarray (developed for 3D, should work on 2D as well)

    Parameters
    ----------
    baseImage : sitk.Image | np.ndarray
        Image to randomly generate pixel values. Can be a sitk.Image or np.ndarray.
    randomSeed : int
        Value to initialize random number generator with. Set for reproducible results.

    Returns
    -------
    sitk.Image | np.ndarray
        Image with all pixel values randomly generated with same dimensions and object type as input image.
    """
    # # Check if baseImage is a sitk.Image or np.ndarray
    arrImage = getArrayFromImageOrArray(baseImage)

    # Get array dimensions to reshape back to
    imgDimensions = arrImage.shape

    # Get min and max HU values to set as range for random values
    minVoxelVal = np.min(arrImage)
    maxVoxelVal = np.max(arrImage)

    # Delete arrImage to save memory
    del arrImage

    # Set the random seed for np random generator
    randNumGen = np.random.default_rng(seed=randomSeed)

    # Generate random array with same dimensions as baseImage with values ranging from the minimum to maximum inclusive of the original image
    random3DArr = randNumGen.integers(
        low=minVoxelVal, high=maxVoxelVal, endpoint=True, size=imgDimensions
    )

    if type(baseImage) == sitk.Image:
        # Convert random array to a sitk Image
        randomImage = sitk.GetImageFromArray(random3DArr)

        # Set the origin/direction/spacing from the original image to the random image
        alignedRandomImage = alignImages(baseImage, randomImage)

        # Return the random image
        return alignedRandomImage
    
    else:
        # Return the random array
        return random3DArr
    
def makeRandomSampleFromDistributionImage(
    baseImage: Union[Image, ndarray],
    randomSeed: Optional[int] = None,
) -> Union[sitk.Image, np.ndarray]:
    """Function to randomly sample all the pixel values the distribution of existing values in a sitk.Image or np.ndarray.

    Parameters
    ----------
    imageToRandomize : sitk.Image | np.ndarray
        Image to randomly sample the pixels from. Can be a sitk.Image or np.ndarray.
    randomSeed : int
        Value to initialize random number generator with. Set for reproducible results.
    Returns
    -------
    sitk.Image | np.ndarray
        Image with all pixel values randomly sampled from the initial dstribution of the image, with same dimensions and object type as input image.
    """
    # Check if baseImage is a sitk.Image or np.ndarray
    arrImage = getArrayFromImageOrArray(baseImage)

    # Get array dimensions to reshape back to
    imgDimensions = arrImage.shape

    # Flatten the 3D array to 1D so values can be shuffled
    flatArrImage = arrImage.flatten()

    # Set the random seed for np random number generator
    randNumGen = np.random.default_rng(seed=randomSeed)

    # Randomly sample values for new array from original image distribution
    sampled_array = randNumGen.choice(flatArrImage, size=len(flatArrImage), replace=True)

    # Reshape the array back into the original image dimensions
    randomlySampled3DArrImage = np.reshape(sampled_array, imgDimensions)

    if type(baseImage) == sitk.Image:
        # Convert back to sitk Image
        randomlySampledImage = sitk.GetImageFromArray(randomlySampled3DArrImage)

        # Set the origin/direction/spacing from original image to sampled image
        alignedRandomlySampledImage = alignImages(baseImage, randomlySampledImage)
        
        # Return the randomly sampled image 
        return alignedRandomlySampledImage
    else:
        # Return the randomly sampled array
        return randomlySampled3DArrImage

def negativeControlROIOnly(
        baseImage: Union[Image, ndarray], 
        roiMask: Union[Image, ndarray], 
        negativeControlType: str = "shuffled",
        randomSeed: Optional[int] = None
        ) -> Union[Image, ndarray]:
    """Function to apply a negative control to a ROI only, without changing the background of the image.

    Parameters
    ----------
    baseImage : sitk.Image | np.ndarray
        Image to apply negative control to. Can be a sitk.Image or np.ndarray.
    roiMask : sitk.Image | np.ndarray
        Mask of the ROI to apply negative control within. Can be a sitk.Image or np.ndarray.
    negativeControlType : {'shuffled', 'randomized', 'randomized_sampled'}, default 'shuffled'
        Name of negative control to apply.
    randomSeed : int, default None    
        Value to initialize random number generator with. Set for reproducible results.
    
    Returns
    -------
    sitk.Image | np.ndarray
        Image with negative control function applied to all pixel values within the ROI.
    """

    if negativeControlType not in ["shuffled", "randomized", "randomized_sampled"]:
        raise ValueError("negativeControlType must be one of 'shuffled', 'randomized', or 'randomized_sampled'")
    
    # Check if baseImage is a sitk.Image or np.ndarray
    arrBaseImage = getArrayFromImageOrArray(baseImage)
    
    # Check if roiMask is a sitk.Image or np.ndarray
    arrROIMask = getArrayFromImageOrArray(roiMask)

    # Get binary segmentation masks
    # ROI is 1, background is 0
    binROIMask = np.where(arrROIMask > 0, 1, 0)
    if binROIMask.any() == False:
        raise ValueError("ROI mask is all 0s. No pixels in ROI to apply negative control to. ROI pixels should be > 1.")

    # Get just ROI pixels
    maskIndices = np.nonzero(binROIMask)
    # Get a 1D array of just the ROI pixels
    flatROIBaseValues = arrBaseImage[maskIndices]

    # Get desired negative control of baseImage
    arrNCROIValues = applyNegativeControl(baseImage = flatROIBaseValues,
                                          negativeControlType = negativeControlType,
                                          negativeControlRegion = "full",
                                          randomSeed = randomSeed)

    arrBaseImage[maskIndices] = arrNCROIValues

    # # Apply negative control to ROI pixels and keep original non-ROI pixels
    # arrNCROIImage = (arrNCBaseImage * binROIMask) + (arrBaseImage * inverseBinROIMask)

    if type(baseImage) == sitk.Image:
        # Convert back to sitk Image
        ncROIImage = sitk.GetImageFromArray(arrBaseImage)
        
        # Set the origin/direction/spacing from original image to negative control image
        alignedNCROIImage = alignImages(baseImage, ncROIImage)
        
        # Return the negative control image
        return alignedNCROIImage
    else:
        # Return the negative control array
        return arrBaseImage


def negativeControlNonROIOnly(
        baseImage: Union[Image, ndarray], 
        roiMask: Union[Image, ndarray], 
        negativeControlType: str = "shuffled",
        randomSeed: Optional[int] = None
        ) -> Union[Image, ndarray]:
    """Function to apply a negative control to all pixel values outside the ROI, without changing the ROI pixels.

    Parameters
    ----------
    baseImage : sitk.Image | np.ndarray
        Image to apply negative control to. Can be a sitk.Image or np.ndarray.
    roiMask : sitk.Image | np.ndarray
        Mask of the ROI to keep original image values within. Can be a sitk.Image or np.ndarray.
    negativeControlType : {'shuffled', 'randomized', 'randomized_sampled'}, default 'shuffled'
        Name of negative control to apply.
    randomSeed : int, default None    
        Value to initialize random number generator with. Set for reproducible results.
    
    Returns
    -------
    sitk.Image | np.ndarray
        Image with negative control function applied to all pixel values within the ROI.
    """

    if negativeControlType not in ["shuffled", "randomized", "randomized_sampled"]:
        raise ValueError("negativeControlType must be one of 'shuffled', 'randomized', or 'randomized_sampled'")
    
    # Check if baseImage is a sitk.Image or np.ndarray
    arrBaseImage = getArrayFromImageOrArray(baseImage)

    # Check if roiMask is a sitk.Image or np.ndarray
    arrROIMask = getArrayFromImageOrArray(roiMask)

    # Get binary segmentation masks
    # ROI is 1, background is 0
    binNonROIMask = np.where(arrROIMask > 0, 0, 1)
    if binNonROIMask.any() == False:
        raise ValueError("ROI mask is all 0s. No pixels in ROI to apply negative control to. ROI pixels should be > 1.")

    # Get just ROI pixels
    maskIndices = np.nonzero(binNonROIMask)
    # Get a 1D array of just the ROI pixels
    flatNonROIBaseValues = arrBaseImage[maskIndices]

    # Get desired negative control of baseImage
    arrNCNonROIValues = applyNegativeControl(baseImage = flatNonROIBaseValues,
                                          negativeControlType = negativeControlType,
                                          negativeControlRegion = "full",
                                          randomSeed = randomSeed)
    
    arrBaseImage[maskIndices] = arrNCNonROIValues

    if type(baseImage) == sitk.Image:
        # Convert back to sitk Image
        ncNonROIImage = sitk.GetImageFromArray(arrBaseImage)
        
        # Set the origin/direction/spacing from original image to negative control image
        alignedNCNonROIImage = alignImages(baseImage, ncNonROIImage)
        
        # Return the negative control image
        return alignedNCNonROIImage
    else:
        # Return the negative control array
        return arrBaseImage



def applyNegativeControl(baseImage: Union[Image, ndarray],
                         negativeControlType: str = "shuffled",
                         negativeControlRegion: str = "full",
                         roiMask: Optional[Union[Image, ndarray]] = None,
                         randomSeed: Optional[int] = None
) -> Union[Image, ndarray]:
    """Function to apply a negative control to a region of interest (ROI) within a sitk.Image or np.ndarray.

    Parameters
    ----------
    baseImage : sitk.Image | np.ndarray
        Image to apply negative control to. Can be a sitk.Image or np.ndarray.
    negativeControlType : {'shuffled', 'randomized', 'randomized_sampled'}, default 'shuffled'
        Name of negative control to apply.
    negativeControlRegion : {'full', 'roi', 'non_roi'}, default 'full'
        Whether to apply the negative control to the entire image, to the ROI, or to the non-ROI pixels.
    randomSeed : int, default None    
        Value to initialize random number generator with. Set for reproducible results.
    
    Returns
    -------
    sitk.Image | np.ndarray
        Image with negative control function applied to all pixel values within the specificed region of interest.

    """
    if negativeControlType not in ["shuffled", "randomized", "randomized_sampled"]:
        raise ValueError("negativeControlType must be one of 'shuffled', 'randomized', or 'randomized_sampled'")
    if negativeControlRegion not in ["full", "roi", "non_roi"]:
        raise ValueError("regionOfInterest must be one of 'full', 'roi', or 'non_roi'")
    
    if negativeControlRegion == "full":
        if negativeControlType == "shuffled":
            return makeShuffleImage(baseImage, randomSeed)
        elif negativeControlType == "randomized":
            return makeRandomImage(baseImage, randomSeed)
        elif negativeControlType == "randomized_sampled":
            return makeRandomSampleFromDistributionImage(baseImage, randomSeed)
    
    assert roiMask is not None, \
        f"ROI mask is None. Must pass ROI mask to negative control function for {negativeControlType} negative control."
    
    if negativeControlRegion == "roi":
        return negativeControlROIOnly(baseImage, roiMask, negativeControlType, randomSeed)
    else: # negativeControlRegion == "non_roi":
        return negativeControlNonROIOnly(baseImage, roiMask, negativeControlType, randomSeed)

#################################################################
####################### OLD FUNCTIONS ###########################
#################################################################
# def makeRandomRoi(
#     baseImage: sitk.Image, 
#     baseROI: sitk.Image, 
#     roiLabel: Optional[int] = None,
#     randomSeed: Optional[int] = None
# ) -> sitk.Image:
#     """Function to generate random pixel values within the Region of Interest based on the range of values in a sitk Image

#     Parameters
#     ----------
#     baseImage : sitk.Image
#         Image to randomly generate pixel values in Region of Interest
#     baseROI : sitk.Image
#         Image detailing Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.
        
#     Returns
#     -------
#     sitk.Image
#         Image with all pixel values within the Region of Interest randomly generated with same dimensions as input image
#     """
#     # Check the ROI Label exists, if not extract it manually
#     if not roiLabel:
#         roiLabel = getROIVoxelLabel(baseROI)

#     # Initialize variables to track the highest and lowest pixel values in the ROI
#     maxVoxelVal = float("-inf")
#     minVoxelVal = float("inf")

#     # Iterate through baseROI to find the highest and lowest values in baseImage's ROI
#     baseROISize = baseROI.GetSize()
#     for x in range(baseROISize[0]):
#         for y in range(baseROISize[1]):
#             for z in range(baseROISize[2]):
#                 # Ensure only pixels that match the roiLabel of hte image are looked at
#                 if baseROI.GetPixel(x, y, z) == roiLabel:
#                     # Once a pixel is confirmed to be in the ROI get it's corresponding value from the baseImage
#                     current_value = baseImage.GetPixel(x, y, z)
#                     # Update the max and min values
#                     maxVoxelVal = max(maxVoxelVal, current_value)
#                     minVoxelVal = min(minVoxelVal, current_value)

#     # Create a new base image so we are not directly editing the input image
#     new_base = baseImage.__copy__()
#     # Delete the input image to save space
#     del baseImage

#     # Set the random seed for np random generator
#     randNumGen = np.random.default_rng(seed=randomSeed)

#     # Now iterate over the pixels of the ROI in the image and randomly generate a new value for them
#     for x in range(baseROISize[0]):
#         for y in range(baseROISize[1]):
#             for z in range(baseROISize[2]):
#                 if baseROI.GetPixel(x, y, z) == roiLabel:
#                     # Randomly assigning the current value to the range [maxVoxelVal, maxVoxelVal]
#                     mapped_value = int(randNumGen.integers(low=minVoxelVal, high=maxVoxelVal, endpoint=True))

#                     # Set the new pixel value
#                     new_base.SetPixel(x, y, z, mapped_value)

#     return new_base


# def shuffleROI(
#     baseImage: sitk.Image, 
#     baseROI: sitk.Image, 
#     roiLabel: Optional[int] = None,
#     randomSeed: Optional[int] = None,
# ) -> sitk.Image:
#     """Function to shuffle all pixel values within the Region of Interest in a sitk Image

#     Parameters
#     ----------
#     baseImage : sitk.Image
#         Image to shuffle the Region of Interest pixels in
#     baseROI : sitk.Image
#         Image detailing Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.
        
#     Returns
#     -------
#     sitk.Image
#         Image with all pixel values in the Region of Interest randomly shuffled with same dimensions as input image
#     """
#     # Check the ROI Label exists, if not extract it manually
#     if not roiLabel:
#         roiLabel = getROIVoxelLabel(baseROI)

#     # A collection of corresponding value in the BaseImage of all the pixels in the ROI
#     count = []
#     # Iterate through baseROI to store the corresponding value in the baseImage of all the pixels in the ROI
#     baseROISize = baseROI.GetSize()
#     for x in range(baseROISize[0]):
#         for y in range(baseROISize[1]):
#             for z in range(baseROISize[2]):
#                 if baseROI.GetPixel(x, y, z) == roiLabel:
#                     # append the ROI corresponding pixel values to the list
#                     count.append(baseImage.GetPixel(x, y, z))

#     # Create a new base image so we are not directly editing the input image
#     new_base = baseImage.__copy__()
#     # Delete the input image to save space
#     del baseImage

#     # Initialize the random number generator
#     random.seed(randomSeed)
#     # Randomly shuffling the pixel values
#     random.shuffle(count)

#     for x in range(baseROISize[0]):
#         for y in range(baseROISize[1]):
#             for z in range(baseROISize[2]):
#                 if baseROI.GetPixel(x, y, z) == roiLabel:
#                     # Set the value of a pixel in the ROI to be a shuffled value
#                     new_base.SetPixel(x, y, z, count.pop())

#     return new_base


# def makeRandomNonRoi(
#     baseImage: sitk.Image, 
#     baseROI: sitk.Image,
#     roiLabel: Optional[int] = None,
#     randomSeed: Optional[int] = None
# ) -> sitk.Image:
#     """Function to generate random pixel values outside the Region of Interest based on the range of values in a sitk Image

#     Parameters
#     ----------
#     baseImage : sitk.Image
#         Image to randomly generate pixel values in outside the Region of Interest
#     baseROI : sitk.Image
#         Image detailing the Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.

#     Returns
#     -------
#     sitk.Image
#         Image with all pixel values outside the Region of Interest randomly generated with same dimensions as input image
#     """
#     # Check the ROI Label exists, if not extract it manually
#     if not roiLabel:
#         roiLabel = getROIVoxelLabel(baseROI)

#     # Initialize variables to track the highest and lowest pixel values not in the ROI
#     maxVoxelVal: float = float("-inf")
#     minVoxelVal: float = float("inf")

#     # Iterate through baseImage to find the highest and lowest values not in baseImage's ROI
#     baseImageSize = baseImage.GetSize()
#     baseROISize = baseROI.GetSize()
#     for x in range(baseImageSize[0]):
#         for y in range(baseImageSize[1]):
#             for z in range(baseImageSize[2]):
#                 # Ensure only pixels that do not match the roiLabel of the image  or are not in the ROI are looked at
#                 if (
#                     x > baseROISize[0]
#                     or y > baseROISize[1]
#                     or z > baseROISize[2]
#                     or baseROI.GetPixel(x, y, z) != roiLabel
#                 ):
#                     # Once a pixel is confirmed to be outside the ROI, we get it's corresponding value from the baseImage
#                     current_value = baseImage.GetPixel(x, y, z)
#                     # Update the max and min values
#                     maxVoxelVal = max(maxVoxelVal, current_value)
#                     minVoxelVal = min(minVoxelVal, current_value)

#     # Create a new base image so we are not directly editing the input image
#     new_base = baseImage.__copy__()
#     # Delete the input image to save space
#     del baseImage

#     # Set the random seed for np random number generator
#     randNumGen = np.random.default_rng(seed=randomSeed)

#     # Now iterate over the pixels outside the ROI in the image and randomly generate a new value for them
#     for x in range(baseImageSize[0]):
#         for y in range(baseImageSize[1]):
#             for z in range(baseImageSize[2]):
#                 if (
#                     x > baseROISize[0]
#                     or y > baseROISize[1]
#                     or z > baseROISize[2]
#                     or baseROI.GetPixel(x, y, z) != roiLabel
#                 ):
#                     # Randomly assigning the current value to the range [maxVoxelVal, maxVoxelVal]
#                     mapped_value = int(randNumGen.integers(low=minVoxelVal, high=maxVoxelVal, endpoint=True))

#                     # Set the new pixel value
#                     new_base.SetPixel(x, y, z, mapped_value)

#     return new_base


# def shuffleNonROI(
#     baseImage: sitk.Image, 
#     baseROI: sitk.Image,
#     roiLabel: Optional[int] = None,
#     randomSeed: Optional[int] = None,
# ) -> sitk.Image:
#     """Function to shuffle all pixel values that are not within the Region of Interest in a sitk Image

#     Parameters
#     ----------
#     baseImage : sitk.Image
#         Image to shuffle the pixels outside the Region of Interest in
#     baseROI : sitk.Image
#         Image detailing Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.
#     Returns
#     -------
#     sitk.Image
#         Image with all pixel values outside the Region of Interest randomly shuffled with same dimensions as input image
#     """
#     # Check the ROI Label exists, if not extract it manually
#     if not roiLabel:
#         roiLabel = getROIVoxelLabel(baseROI)

#     # A collection of corresponding value in the BaseImage of all the pixels not in the ROI
#     count = []
#     # Iterate through baseImage to store the corresponding value in the baseImage of all the pixels outside the ROI
#     baseImageSize = baseImage.GetSize()
#     baseROISize = baseROI.GetSize()
#     for x in range(baseImageSize[0]):
#         for y in range(baseImageSize[1]):
#             for z in range(baseImageSize[2]):
#                 if (
#                     x > baseROISize[0]
#                     or y > baseROISize[1]
#                     or z > baseROISize[2]
#                     or baseROI.GetPixel(x, y, z) != roiLabel
#                 ):
#                     # Here the key is the pixel coordinate and the value is the value of the pixel in the base image
#                     count.append(baseImage.GetPixel(x, y, z))

#     # Create a new base image so we are not directly editing the input image
#     new_base = baseImage.__copy__()
#     # Delete the input image to save space
#     del baseImage

#     # Initialize the random number generator
#     random.seed(randomSeed)
#     # Randomly shuffling the pixel values
#     random.shuffle(count)

#     for x in range(baseImageSize[0]):
#         for y in range(baseImageSize[1]):
#             for z in range(baseImageSize[2]):
#                 if (
#                     x > baseROISize[0]
#                     or y > baseROISize[1]
#                     or z > baseROISize[2]
#                     or baseROI.GetPixel(x, y, z) != roiLabel
#                 ):
#                     # Set the value of a pixel outside the ROI to be a shuffled value
#                     new_base.SetPixel(x, y, z, count.pop())

#     return new_base





# def makeRandomFromRoiDistribution(
#     baseImage: sitk.Image, 
#     baseROI: sitk.Image, 
#     roiLabel: Optional[int] = None,
#     randomSeed: Optional[int] = None
# ) -> sitk.Image:
#     """Function to randomly sample pixel values within the Region of Interest uniformly from the distribution of pixel values in the ROI region sitk Image

#     Parameters
#     ----------
#     baseImage : sitk.Image
#         Image to randomly generate pixel values in Region of Interest
#     baseROI : sitk.Image
#         Image detailing Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.
        
#     Returns
#     -------
#     sitk.Image
#         Image with all pixel values within the Region of Interest randomly sampled with same dimensions as input image
#     """
#     # Check the ROI Label exists, if not extract it manually
#     if not roiLabel:
#         roiLabel = getROIVoxelLabel(baseROI)

#     # Initialize array of ROI pixel distribution
#     distributionROI = []

#     # Iterate through baseROI to find the highest and lowest values in baseImage's ROI
#     baseROISize = baseROI.GetSize()
#     for x in range(baseROISize[0]):
#         for y in range(baseROISize[1]):
#             for z in range(baseROISize[2]):
#                 # Ensure only pixels that match the roiLabel of hte image are looked at
#                 if baseROI.GetPixel(x, y, z) == roiLabel:
#                     # Once a pixel is confirmed to be in the ROI get it's corresponding value from the baseImage
#                     distributionROI.append(baseImage.GetPixel(x, y, z))

#     # Create a new base image so we are not directly editing the input image
#     new_base = baseImage.__copy__()
#     # Delete the input image to save space
#     del (baseImage)

#     # Set the random seed for np random number generator
#     randNumGen = np.random.default_rng(seed=randomSeed)

#     # Now iterate over the pixels of the ROI in the image and randomly generate a new value for them
#     for x in range(baseROISize[0]):
#         for y in range(baseROISize[1]):
#             for z in range(baseROISize[2]):
#                 if baseROI.GetPixel(x, y, z) == roiLabel:
#                     # Assigning the current value to the randomly sampled value from within the ROI
#                     mapped_value = int(randNumGen.choice(distributionROI))

#                     # Set the new pixel value
#                     new_base.SetPixel(x, y, z, mapped_value)

#     return new_base


# def makeRandomNonRoiFromDistribution(
#     baseImage: sitk.Image, 
#     baseROI: sitk.Image, 
#     roiLabel: Optional[int] = None, 
#     randomSeed: Optional[int] = None
# ) -> sitk.Image:
#     """Function to random sample pixel values outside the Region of Interest uniformly from the distribution of pixel values outside the ROI in a sitk Image

#     Parameters
#     ----------
#     baseImage : sitk.Image
#         Image to randomly generate pixel values in outside the Region of Interest
#     baseROI : sitk.Image
#         Image detailing the Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.

#     Returns
#     -------
#     sitk.Image
#         Image with all pixel values outside the Region of Interest randomly sample form outside the ROI with same dimensions as input image
#     """
#     # Check the ROI Label exists, if not extract it manually
#     if not roiLabel:
#         roiLabel = getROIVoxelLabel(baseROI)

#     # Initialize array of non-ROI pixel distribution
#     distributionROI = []

#     # Iterate through baseImage to find the highest and lowest values not in baseImage's ROI
#     baseImageSize = baseImage.GetSize()
#     baseROISize = baseROI.GetSize()
#     for x in range(baseImageSize[0]):
#         for y in range(baseImageSize[1]):
#             for z in range(baseImageSize[2]):
#                 # Ensure only pixels that do not match the roiLabel of the image  or are not in the ROI are looked at
#                 if (
#                     x > baseROISize[0]
#                     or y > baseROISize[1]
#                     or z > baseROISize[2]
#                     or baseROI.GetPixel(x, y, z) != roiLabel
#                 ):
#                     # Once a pixel is confirmed to be outside the ROI, we get it's corresponding value from the baseImage
#                     distributionROI.append(baseImage.GetPixel(x, y, z))

#     # Create a new base image so we are not directly editing the input image
#     new_base = baseImage.__copy__()
#     # Delete the input image to save space
#     del baseImage

#     # Set the random seed for np random number generator
#     randNumGen = np.random.default_rng(seed=randomSeed)

#     # Now iterate over the pixels outside the ROI in the image and randomly generate a new value for them
#     for x in range(baseImageSize[0]):
#         for y in range(baseImageSize[1]):
#             for z in range(baseImageSize[2]):
#                 if (
#                     x > baseROISize[0]
#                     or y > baseROISize[1]
#                     or z > baseROISize[2]
#                     or baseROI.GetPixel(x, y, z) != roiLabel
#                 ):
#                     # Assigning the current value to the randomly sampled value from within the ROI
#                     mapped_value = int(randNumGen.choice(distributionROI))

#                     # Set the new pixel value
#                     new_base.SetPixel(x, y, z, mapped_value)

#     return new_base


# def applyNegativeControl(
#     nc_type: str,
#     baseImage: sitk.Image,
#     baseROI: Optional[sitk.Image] = None,
#     roiLabel: Optional[int] = None,
#     randomSeed: Optional[int] = None
# ) -> sitk.Image:
#     """Function to generate random pixel values within the Region of Interest based on the range of values in a sitk Image

#     Parameters
#     ----------
#     nc_type : str
#         The type of negative control to be applied
#     baseImage : sitk.Image
#         The image to be modified
#     baseROI : sitk.Image
#         Image detailing Region of Interest
#     roiLabel : int
#         The label representing the ROI in baseROI
#     randomSeed : int
#         Value to initialize random number generator with for shuffling. Set for reproducible results.
        
#     Returns
#     -------
#     sitk.Image
#         The output image with the negative control applied
        
#     Raises
#     ------
#     ValueError
#         If the nc_type is not a valid negative control type
#     """
    
#     if nc_type == "randomized_full":
#         # Make negative control version of ctImage (randomized pixel size)
#         return makeRandomImage(baseImage, randomSeed)
#     elif nc_type == "shuffled_full":
#         # Make negative control version of ctImage (random shuffled pixels, same size)
#         return shuffleImage(baseImage, randomSeed)
#     elif nc_type == "randomized_sampled_full":
#         # Make negative control version of ctImage (random sampled pixels from original distribution, same size)
#         return randomizeImageFromDistributionSampling(baseImage, randomSeed)
    
#     # typesafety check here to ensure baseROI is not None for the following negative control types
#     assert baseROI is not None, \
#         f"baseROI must be provided for {nc_type} negative control type"
    
#     if nc_type == "randomized_roi":
#         # Make negative control version of ctImage (randomized pixel size inside the ROI)
#         return makeRandomRoi(baseImage, baseROI, roiLabel, randomSeed)
#     elif nc_type == "shuffled_roi":
#         # Make negative control version of ctImage (random shuffled pixels inside the ROI, same size)
#         return shuffleROI(baseImage, baseROI, roiLabel, randomSeed)
#     elif nc_type == "randomized_non_roi":
#         # Make negative control version of ctImage (randomized pixel size outside the ROI)
#         return makeRandomNonRoi(baseImage, baseROI, roiLabel, randomSeed)
#     elif nc_type == "shuffled_non_roi":
#         # Make negative control version of ctImage (shuffled pixels outside the ROI, same size)
#         return shuffleNonROI(baseImage, baseROI, roiLabel, randomSeed)
#     elif nc_type == "randomized_sampled_roi":
#         # Make negative control version of ctImage (random sampled pixels from original distribution inside ROI, same size)
#         return makeRandomFromRoiDistribution(baseImage, baseROI, roiLabel, randomSeed)
#     elif nc_type == "randomized_sampled_non_roi":
#         # Make negative control version of ctImage (random sampled pixels from original distribution outside ROI, same size)
#         return makeRandomNonRoiFromDistribution(baseImage, baseROI, roiLabel, randomSeed)
#     else:
#         raise ValueError("Invalid nc_type. Please choose a valid negative control type.")
