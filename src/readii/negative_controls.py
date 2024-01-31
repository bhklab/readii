import SimpleITK as sitk
import numpy as np
import random

from readii.image_processing import alignImages


def shuffleImage(imageToShuffle: sitk.Image):
    """Function to shuffle all pixel values in a sitk Image (developed for 3D, should work on 2D as well)

    Parameters
    ----------
    imageToShuffle : sitk.Image
        Image to shuffle the pixels in

    Returns
    -------
    sitk.Image
        Image with all pixel values randomly shuffled with same dimensions as input image
    """
    # Convert the image to an array
    arrImage = sitk.GetArrayFromImage(imageToShuffle)

    # Get array dimensions to reshape back to
    imgDimensions = arrImage.shape

    # Flatten the 3D array to 1D so values can be shuffled
    flatArrImage = arrImage.flatten()

    # Shuffle the flat array
    np.random.shuffle(flatArrImage, )

    # Reshape the array back into the original image dimensions
    shuffled3DArrImage = np.reshape(flatArrImage, imgDimensions)

    # Convert back to sitk Image
    shuffledImage = sitk.GetImageFromArray(shuffled3DArrImage)

    # Set the origin/direction/spacing from original image to shuffled image
    alignedShuffledImage = alignImages(imageToShuffle, shuffledImage)

    return alignedShuffledImage


def makeRandomImage(baseImage: sitk.Image):
    """Function to generate random pixel values based on the range of values in a sitk Image (developed for 3D, should work on 2D as well)

    Parameters
    ----------
    baseImage : sitk.Image
        Image to randomly generate pixel values

    Returns
    -------
    sitk.Image
        Image with all pixel values randomly generated with same dimensions as input image
    """
    # Convert the image to an array
    arrImage = sitk.GetArrayFromImage(baseImage)

    # Get array dimensions to reshape back to
    imgDimensions = arrImage.shape

    # Get min and max HU values to set as range for random values
    minVoxelVal = np.min(arrImage)
    maxVoxelVal = np.max(arrImage)

    # Delete arrImage to save memory
    del (arrImage)

    # Generate random array with same dimensions as baseImage
    random3DArrImage = np.random.randint(low=minVoxelVal, high=maxVoxelVal, size=imgDimensions)

    # Convert random array to a sitk Image
    randomImage = sitk.GetImageFromArray(random3DArrImage)

    # Set the origin/direction/spacing from the original image to the random image
    alignedRandomImage = alignImages(baseImage, randomImage)

    return alignedRandomImage


def makeRandomRoi(baseImage: sitk.Image, baseROI: sitk.Image, roiLabel: int = 1):
    """Function to generate random pixel values within the Region of Interest based on the range of values in a sitk Image

    Parameters
    ----------
    baseImage : sitk.Image
        Image to randomly generate pixel values in Region of Interest
    baseROI : sitk.Image 
        Image detailing Region of Interest
    roiLabel : int
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        Image with all pixel values within the Region of Interest randomly generated with same dimensions as input image
    """
    # Initialize variables to track the highest and lowest pixel values in the ROI
    maxVoxelVal = float('-inf')
    minVoxelVal = float('inf')

    # Iterate through baseROI to find the highest and lowest values in baseImage's ROI
    baseROISize = baseROI.GetSize()
    for x in range(baseROISize[0]):
        for y in range(baseROISize[1]):
            for z in range(baseROISize[2]):
                # Ensure only pixels that match the roiLabel of hte image are looked at
                if baseROI.GetPixel(x, y, z) == roiLabel:
                    # Once a pixel is confirmed to be in the ROI get it's corresponding value from the baseImage
                    current_value = baseImage.GetPixel(x, y, z)
                    # Update the max and min values
                    maxVoxelVal = max(maxVoxelVal, current_value)
                    minVoxelVal = min(minVoxelVal, current_value)

    # Create a new base image so we are not directly editing the input image
    new_base = baseImage.__copy__()
    # Delete the input image to save space
    del (baseImage)

    # Now iterate over the pixels of the ROI in the image and randomly generate a new value for them
    for x in range(baseROISize[0]):
        for y in range(baseROISize[1]):
            for z in range(baseROISize[2]):
                if baseROI.GetPixel(x, y, z) == roiLabel:
                    # Randomly assigning the current value to the range [maxVoxelVal, maxVoxelVal]
                    mapped_value = random.randint(minVoxelVal, maxVoxelVal)

                    # Set the new pixel value
                    new_base.SetPixel(x, y, z, mapped_value)

    return new_base


def shuffleROI(baseImage: sitk.Image, baseROI: sitk.Image, roiLabel: int = 1):
    """Function to shuffle all pixel values within the Region of Interest in a sitk Image

    Parameters
    ----------
    baseImage : sitk.Image
        Image to shuffle the Region of Interest pixels in
    baseROI : sitk.Image
        Image detailing Region of Interest
    roiLabel : int
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        Image with all pixel values in the Region of Interest randomly shuffled with same dimensions as input image
    """

    # A collection of corresponding value in the BaseImage of all the pixels in the ROI
    count = []
    # Iterate through baseROI to store the corresponding value in the baseImage of all the pixels in the ROI
    baseROISize = baseROI.GetSize()
    for x in range(baseROISize[0]):
        for y in range(baseROISize[1]):
            for z in range(baseROISize[2]):
                if baseROI.GetPixel(x, y, z) == roiLabel:
                    # append the ROI corresponding pixel values to the list
                    count.append(baseImage.GetPixel(x, y, z))

    # Create a new base image so we are not directly editing the input image
    new_base = baseImage.__copy__()
    # Delete the input image to save space
    del (baseImage)

    # # Randomly shuffling the pixel values
    random.shuffle(count)

    for x in range(baseROISize[0]):
        for y in range(baseROISize[1]):
            for z in range(baseROISize[2]):
                if baseROI.GetPixel(x, y, z) == roiLabel:
                    # Set the value of a pixel in the ROI to be a shuffled value
                    new_base.SetPixel(x, y, z, count.pop())

    return new_base


def makeRandomNonRoi(baseImage: sitk.Image, baseROI: sitk.Image, roiLabel: int = 1):
    """Function to generate random pixel values outside the Region of Interest based on the range of values in a sitk Image

    Parameters
    ----------
    baseImage : sitk.Image
        Image to randomly generate pixel values in outside the Region of Interest
    baseROI : sitk.Image
        Image detailing the Region of Interest
    roiLabel : int 
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        Image with all pixel values outside the Region of Interest randomly generated with same dimensions as input image
    """
    # Initialize variables to track the highest and lowest pixel values not in the ROI
    maxVoxelVal = float('-inf')
    minVoxelVal = float('inf')

    # Iterate through baseImage to find the highest and lowest values not in baseImage's ROI
    baseImageSize = baseImage.GetSize()
    baseROISize = baseROI.GetSize()
    for x in range(baseImageSize[0]):
        for y in range(baseImageSize[1]):
            for z in range(baseImageSize[2]):
                # Ensure only pixels that do not match the roiLabel of the image  or are not in the ROI are looked at
                if x > baseROISize[0] or y > baseROISize[1] or z > baseROISize[2] or baseROI.GetPixel(x, y,
                                                                                                      z) != roiLabel:
                    # Once a pixel is confirmed to be outside the ROI, we get it's corresponding value from the baseImage
                    current_value = baseImage.GetPixel(x, y, z)
                    # Update the max and min values
                    maxVoxelVal = max(maxVoxelVal, current_value)
                    minVoxelVal = min(minVoxelVal, current_value)

    # Create a new base image so we are not directly editing the input image
    new_base = baseImage.__copy__()
    # Delete the input image to save space
    del (baseImage)

    # Now iterate over the pixels outside the ROI in the image and randomly generate a new value for them
    for x in range(baseImageSize[0]):
        for y in range(baseImageSize[1]):
            for z in range(baseImageSize[2]):
                if x > baseROISize[0] or y > baseROISize[1] or z > baseROISize[2] or baseROI.GetPixel(x, y,
                                                                                                      z) != roiLabel:
                    # Randomly assigning the current value to the range [maxVoxelVal, maxVoxelVal]
                    mapped_value = random.randint(minVoxelVal, maxVoxelVal)

                    # Set the new pixel value
                    new_base.SetPixel(x, y, z, mapped_value)

    return new_base


def shuffleNonROI(baseImage: sitk.Image, baseROI: sitk.Image, roiLabel: int = 1):
    """Function to shuffle all pixel values that are not within the Region of Interest in a sitk Image

    Parameters
    ----------
    baseImage : sitk.Image
        Image to shuffle the pixels outside the Region of Interest in
    baseROI : sitk.Image
        Image detailing Region of Interest
    roiLabel : int
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        Image with all pixel values outside the Region of Interest randomly shuffled with same dimensions as input image
    """

    # A collection of corresponding value in the BaseImage of all the pixels not in the ROI
    count = []
    # Iterate through baseImage to store the corresponding value in the baseImage of all the pixels outside the ROI
    baseImageSize = baseImage.GetSize()
    baseROISize = baseROI.GetSize()
    for x in range(baseImageSize[0]):
        for y in range(baseImageSize[1]):
            for z in range(baseImageSize[2]):
                if x > baseROISize[0] or y > baseROISize[1] or z > baseROISize[2] or baseROI.GetPixel(x, y,
                                                                                                      z) != roiLabel:
                    # Here the key is the pixel coordinate and the value is the value of the pixel in the base image
                    count.append(baseImage.GetPixel(x, y, z))

    # Create a new base image so we are not directly editing the input image
    new_base = baseImage.__copy__()
    # Delete the input image to save space
    del (baseImage)

    # Randomly shuffling the pixel values
    random.shuffle(count)

    for x in range(baseImageSize[0]):
        for y in range(baseImageSize[1]):
            for z in range(baseImageSize[2]):
                if x > baseROISize[0] or y > baseROISize[1] or z > baseROISize[2] or baseROI.GetPixel(x, y,
                                                                                                      z) != roiLabel:
                    # Set the value of a pixel outside the ROI to be a shuffled value
                    new_base.SetPixel(x, y, z, count.pop())

    return new_base

def randomizeImageFromDistribtutionSampling(imageToRandomize: sitk.Image):
    """Function to randomly sample all the pixel values in a sitk Image, from the distribution of existing values

    Parameters
    ----------
    imageToRandomize : sitk.Image
        Image to randomly sample the pixels in

    Returns
    -------
    sitk.Image
        Image with all pixel values randomly sampled from the initial dstribution of the image, with same dimensions as input image
    """
    # Convert the image to an array
    arrImage = sitk.GetArrayFromImage(imageToRandomize)

    # Get array dimensions to reshape back to
    imgDimensions = arrImage.shape

    # Flatten the 3D array to 1D so values can be shuffled
    flatArrImage = arrImage.flatten()

    # Randomly sample values for new array from original image distribution
    sampled_array = np.random.choice(flatArrImage, size=len(flatArrImage), replace=True)

    # Reshape the array back into the original image dimensions
    randomlySampled3DArrImage = np.reshape(sampled_array, imgDimensions)

    # Convert back to sitk Image
    randomlySampledImage = sitk.GetImageFromArray(randomlySampled3DArrImage)

    # Set the origin/direction/spacing from original image to sampled image
    alignedRandomlySampledImage = alignImages(imageToRandomize, randomlySampledImage)

    return alignedRandomlySampledImage

def makeRandomFromRoiDistribution(baseImage: sitk.Image, baseROI: sitk.Image, roiLabel: int = 1):
    """Function to randomly sample pixel values within the Region of Interest uniformly from the distribution of pixel values in the ROI region sitk Image

    Parameters
    ----------
    baseImage : sitk.Image
        Image to randomly generate pixel values in Region of Interest
    baseROI : sitk.Image
        Image detailing Region of Interest
    roiLabel : int
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        Image with all pixel values within the Region of Interest randomly sampled with same dimensions as input image
    """
    # Initialize array of ROI pixel distribution
    distributionROI = []

    # Iterate through baseROI to find the highest and lowest values in baseImage's ROI
    baseROISize = baseROI.GetSize()
    for x in range(baseROISize[0]):
        for y in range(baseROISize[1]):
            for z in range(baseROISize[2]):
                # Ensure only pixels that match the roiLabel of hte image are looked at
                if baseROI.GetPixel(x, y, z) == roiLabel:
                    # Once a pixel is confirmed to be in the ROI get it's corresponding value from the baseImage
                    distributionROI.append(baseImage.GetPixel(x, y, z))

    # Create a new base image so we are not directly editing the input image
    new_base = baseImage.__copy__()
    # Delete the input image to save space
    del (baseImage)

    # Now iterate over the pixels of the ROI in the image and randomly generate a new value for them
    for x in range(baseROISize[0]):
        for y in range(baseROISize[1]):
            for z in range(baseROISize[2]):
                if baseROI.GetPixel(x, y, z) == roiLabel:
                    # Assigning the current value to the randomly sampled value from within the ROI
                    mapped_value = random.choice(distributionROI)

                    # Set the new pixel value
                    new_base.SetPixel(x, y, z, mapped_value)

    return new_base

def makeRandomNonRoiFromDistribution(baseImage: sitk.Image, baseROI: sitk.Image, roiLabel: int = 1):
    """Function to random sample pixel values outside the Region of Interest uniformly from the distribution of pixel values outside the ROI in a sitk Image

    Parameters
    ----------
    baseImage : sitk.Image
        Image to randomly generate pixel values in outside the Region of Interest
    baseROI : sitk.Image
        Image detailing the Region of Interest
    roiLabel : int
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        Image with all pixel values outside the Region of Interest randomly sample form outside the ROI with same dimensions as input image
    """

    # Initialize array of non-ROI pixel distribution
    distributionROI = []

    # Iterate through baseImage to find the highest and lowest values not in baseImage's ROI
    baseImageSize = baseImage.GetSize()
    baseROISize = baseROI.GetSize()
    for x in range(baseImageSize[0]):
        for y in range(baseImageSize[1]):
            for z in range(baseImageSize[2]):
                # Ensure only pixels that do not match the roiLabel of the image  or are not in the ROI are looked at
                if x > baseROISize[0] or y > baseROISize[1] or z > baseROISize[2] or baseROI.GetPixel(x, y,
                                                                                                      z) != roiLabel:
                    # Once a pixel is confirmed to be outside the ROI, we get it's corresponding value from the baseImage
                    distributionROI.append(baseImage.GetPixel(x, y, z))

    # Create a new base image so we are not directly editing the input image
    new_base = baseImage.__copy__()
    # Delete the input image to save space
    del (baseImage)

    # Now iterate over the pixels outside the ROI in the image and randomly generate a new value for them
    for x in range(baseImageSize[0]):
        for y in range(baseImageSize[1]):
            for z in range(baseImageSize[2]):
                if x > baseROISize[0] or y > baseROISize[1] or z > baseROISize[2] or baseROI.GetPixel(x, y,
                                                                                                      z) != roiLabel:
                    # Assigning the current value to the randomly sampled value from within the ROI
                    mapped_value = random.choice(distributionROI)

                    # Set the new pixel value
                    new_base.SetPixel(x, y, z, mapped_value)

    return new_base


def applyNegativeControl(nc_type: str, baseImage: sitk.Image, baseROI: sitk.Image = None, roiLabel: int = 1):
    """Function to generate random pixel values within the Region of Interest based on the range of values in a sitk Image

    Parameters
    ----------
    nc_type : str
        The type of negative control to be applied
    baseImage : sitk.Image
        The image to be modified
    baseROI : sitk.Image
        Image detailing Region of Interest
    roiLabel : int
        The label representing the ROI in baseROI

    Returns
    -------
    sitk.Image
        The output image with the negative control applied
     """

    if nc_type == "randomized_full":
        # Make negative control version of ctImage (randomized pixel size)
        return makeRandomImage(baseImage)
    elif nc_type == "randomized_roi":
        # Make negative control version of ctImage (randomized pixel size inside the ROI)
        return makeRandomRoi(baseImage, baseROI, roiLabel)
    elif nc_type == "shuffled_roi":
        # Make negative control version of ctImage (random shuffled pixels inside the ROI, same size)
        return shuffleROI(baseImage, baseROI, roiLabel)
    elif nc_type == "randomized_non_roi":
        # Make negative control version of ctImage (randomized pixel size outside the ROI)
        return makeRandomNonRoi(baseImage, baseROI, roiLabel)
    elif nc_type == "shuffled_non_roi":
        # Make negative control version of ctImage (shuffled pixels outside the ROI, same size)
        return shuffleNonROI(baseImage, baseROI, roiLabel)
    elif nc_type == "randomized_sampled_full":
        # Make negative control version of ctImage (random sampled pixels from original distribution, same size)
        return randomizeImageFromDistribtutionSampling(baseImage)
    elif nc_type == "randomized_sampled_roi":
        # Make negative control version of ctImage (random sampled pixels from original distribution inside ROI, same size)
        return makeRandomFromRoiDistribution(baseImage, baseROI, roiLabel)
    elif nc_type == "randomized_sampled_non_roi":
        # Make negative control version of ctImage (random sampled pixels from original distribution outside ROI, same size)
        return makeRandomNonRoiFromDistribution(baseImage, baseROI, roiLabel)
    elif nc_type == "shuffled_full":
        # Make negative control version of ctImage (random shuffled pixels, same size)
        return shuffleImage(baseImage)
