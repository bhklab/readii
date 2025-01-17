import numpy as np
import SimpleITK as sitk
from imgtools.ops.functional import resample

from readii.utils import logger


def resizeImage(image:sitk.Image,
                resized_dimensions:tuple
                ) -> sitk.Image:
    """Resize an image to specified dimensions via linear interpolation.

    Parameters
    ----------
    image : sitk.Image
        Image to resize.
    resized_dimensions : tuple
        Tuple of integers representing the new dimensions to resize the image to. Must have the same number of dimensions as the image.

    Returns
    -------
    resized_image : sitk.Image
        Resized image.
    """
    # Check that the number of dimensions in the resized dimensions matches the number of dimensions in the image
    if len(resized_dimensions) != image.GetDimension():
        msg = f"Number of dimensions in resized_dimensions ({len(resized_dimensions)}) does not match the number of dimensions in the image ({image.GetDimension()})."
        logger.exception(msg)
        raise ValueError(msg)
    
    # Check that the resized dimensions are integers
    if not all(isinstance(dim, int) for dim in resized_dimensions):
        msg = "Resized dimensions must be integers."
        logger.exception(msg)
        raise ValueError(msg)
    
    # Calculate the new spacing based on the resized dimensions
    original_dimensions = np.array(image.GetSize())
    original_spacing = np.array(image.GetSpacing())
    resized_spacing = original_spacing * original_dimensions / resized_dimensions

    # Resample the image to the new dimensions and spacing
    resized_image = resample(image, spacing=resized_spacing, size=resized_dimensions)

    return resized_image
    

