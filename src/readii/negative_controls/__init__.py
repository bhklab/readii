from .base import NegativeControl  # noqa: I001
from .enums import NegativeControlRegion, NegativeControlType
from .factory import NegativeControlFactory
from .registry import NegativeControlRegistry

# Import the implemented classes so they get registered along with the registry
#      This is because if module (e.g. randomized.py) is never imported, then it isn't run and
#      thus not registered with the registry
# Alternatively, can use a more plugin-like approach where all modules are dynamically
# imported and thus registered using pkgutil and importlib
from .random_sample import RandomizedSampledControl
from .randomized import RandomizedControl
from .shuffled import ShuffledControl

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
    """Convert a SimpleITK Image to a numpy array.

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
    assert isinstance(imageOrArray, Image) or isinstance(
        imageOrArray, ndarray
    ), "Input must be a SimpleITK Image or numpy array."

    if isinstance(imageOrArray, Image):
        return sitk.GetArrayFromImage(imageOrArray)
    elif isinstance(imageOrArray, ndarray):
        return imageOrArray


def makeShuffleImage(
    baseImage: Union[Image, ndarray],
    randomSeed: Optional[int] = None,
) -> Union[Image, ndarray]:
    """Shuffle all pixel values in a sitk.Image or np.ndarray (developed for 3D, should work on 2D as well).

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
    """Generate random pixel values based on the range of values in a sitk.Image or np.ndarray 

    (developed for 3D, should work on 2D as well).

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
    """Randomly sample all pixel values from existing values in a sitk.Image or np.ndarray.

    Parameters
    ----------
    imageToRandomize : sitk.Image | np.ndarray
        Image to randomly sample the pixels from. Can be a sitk.Image or np.ndarray.
    randomSeed : int
        Value to initialize random number generator with. Set for reproducible results.

    Returns
    -------
    sitk.Image | np.ndarray
        Image with all pixel values randomly sampled from the initial dstribution of the image,
        with same dimensions and object type as input image.
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
    randomSeed: Optional[int] = None,
) -> Union[Image, ndarray]:
    """Apply a negative control to a ROI only, without changing the background of the image.

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
        raise ValueError(
            "negativeControlType must be one of 'shuffled', 'randomized', or 'randomized_sampled'"
        )

    # Check if baseImage is a sitk.Image or np.ndarray
    arrBaseImage = getArrayFromImageOrArray(baseImage)

    # Check if roiMask is a sitk.Image or np.ndarray
    arrROIMask = getArrayFromImageOrArray(roiMask)

    # Get binary segmentation masks
    # ROI is 1, background is 0
    binROIMask = np.where(arrROIMask > 0, 1, 0)
    if binROIMask.any() == False:
        raise ValueError(
            "ROI mask is all 0s. No pixels in ROI to apply negative control to. ROI pixels should be > 1."
        )

    # Get just ROI pixels
    maskIndices = np.nonzero(binROIMask)
    # Get a 1D array of just the ROI pixels
    flatROIBaseValues = arrBaseImage[maskIndices]

    # Get desired negative control of baseImage
    arrNCROIValues = applyNegativeControl(
        baseImage=flatROIBaseValues,
        negativeControlType=negativeControlType,
        negativeControlRegion="full",
        randomSeed=randomSeed,
    )

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
    randomSeed: Optional[int] = None,
) -> Union[Image, ndarray]:
    """Apply a negative control to all pixel values outside the ROI, without changing the ROI pixels.

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
        raise ValueError(
            "negativeControlType must be one of 'shuffled', 'randomized', or 'randomized_sampled'"
        )

    # Check if baseImage is a sitk.Image or np.ndarray
    arrBaseImage = getArrayFromImageOrArray(baseImage)

    # Check if roiMask is a sitk.Image or np.ndarray
    arrROIMask = getArrayFromImageOrArray(roiMask)

    # Get binary segmentation masks
    # ROI is 1, background is 0
    binNonROIMask = np.where(arrROIMask > 0, 0, 1)
    if binNonROIMask.any() == False:
        raise ValueError(
            "ROI mask is all 0s. No pixels in ROI to apply negative control to. ROI pixels should be > 1."
        )

    # Get just ROI pixels
    maskIndices = np.nonzero(binNonROIMask)
    # Get a 1D array of just the ROI pixels
    flatNonROIBaseValues = arrBaseImage[maskIndices]

    # Get desired negative control of baseImage
    arrNCNonROIValues = applyNegativeControl(
        baseImage=flatNonROIBaseValues,
        negativeControlType=negativeControlType,
        negativeControlRegion="full",
        randomSeed=randomSeed,
    )

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


def applyNegativeControl(
    baseImage: Union[Image, ndarray],
    negativeControlType: str = "shuffled",
    negativeControlRegion: str = "full",
    roiMask: Optional[Union[Image, ndarray]] = None,
    randomSeed: Optional[int] = None,
) -> Union[Image, ndarray]:
    """Apply a negative control to a region of interest (ROI) within a sitk.Image or np.ndarray.

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
        raise ValueError(
            "negativeControlType must be one of 'shuffled', 'randomized', or 'randomized_sampled'"
        )
    if negativeControlRegion not in ["full", "roi", "non_roi"]:
        raise ValueError("regionOfInterest must be one of 'full', 'roi', or 'non_roi'")

    if negativeControlRegion == "full":
        if negativeControlType == "shuffled":
            return makeShuffleImage(baseImage, randomSeed)
        elif negativeControlType == "randomized":
            return makeRandomImage(baseImage, randomSeed)
        elif negativeControlType == "randomized_sampled":
            return makeRandomSampleFromDistributionImage(baseImage, randomSeed)

    assert (
        roiMask is not None
    ), f"ROI mask is None. Must pass ROI mask to negative control function for {negativeControlType} negative control."

    if negativeControlRegion == "roi":
        return negativeControlROIOnly(baseImage, roiMask, negativeControlType, randomSeed)
    else:  # negativeControlRegion == "non_roi":
        return negativeControlNonROIOnly(baseImage, roiMask, negativeControlType, randomSeed)

