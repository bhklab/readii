
import numpy as np
import SimpleITK as sitk
from imgtools.ops.functional import resample

from readii.utils import logger


def validateNewDimensions(image:sitk.Image,
                          new_dimensions:tuple
                          ) -> None:
    """Validate that the input new dimensions are valid for the image.

    Parameters
    ----------
    image : sitk.Image
        Image to validate the new dimensions for.
    new_dimensions : tuple
        Tuple of integers representing the new dimensions to validate.

    Raises
    ------
    ValueError
        If the new dimensions are not valid for the image.
    """
    # Check that the number of dimensions in the new dimensions matches the number of dimensions in the image
    if len(new_dimensions) != image.GetDimension():
        msg = f"Number of dimensions in new_dimensions ({len(new_dimensions)}) does not match the number of dimensions in the image ({image.GetDimension()})."
        logger.exception(msg)
        raise ValueError(msg)
    
    # Check that the new dimensions are integers
    if not all(isinstance(dim, int) for dim in new_dimensions):
        msg = "New dimensions must be integers."
        logger.exception(msg)
        raise ValueError(msg)



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
    validateNewDimensions(image, resized_dimensions)
    
    # Calculate the new spacing based on the resized dimensions
    original_dimensions = np.array(image.GetSize())
    original_spacing = np.array(image.GetSpacing())
    resized_spacing = original_spacing * original_dimensions / resized_dimensions

    # Resample the image to the new dimensions and spacing
    resized_image = resample(image, spacing=resized_spacing, size=resized_dimensions)

    return resized_image
    


def findBoundingBox(mask:sitk.Image,
                    min_dim_size:int = 4) -> np.ndarray:
    """Find the bounding box of a region of interest (ROI) in a given binary mask image.
    
    Parameters
    ----------
    mask : sitk.Image
        Mask image to find the bounding box within.
    min_dim_size : int, optional
        Minimum size of the bounding box along each dimension. The default is 4.
    
    Returns
    -------
    bounding_box : np.ndarray
        Numpy array containing the bounding box coordinates around the ROI.
    """
    # Convert the mask to a uint8 image
    mask_uint = sitk.Cast(mask, sitk.sitkUInt8)
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(mask_uint)
    # Get the bounding box starting coordinates and size
    xstart, ystart, zstart, xsize, ysize, zsize = stats.GetBoundingBox(1)

    # Ensure minimum size of 4 pixels along each dimension
    xsize = max(xsize, min_dim_size)
    ysize = max(ysize, min_dim_size)
    zsize = max(zsize, min_dim_size)

    min_coord = [xstart, ystart, zstart]
    # Calculate the maximum coordinate of the bounding box by adding the size to the starting coordinate
    max_coord = [xstart + xsize, ystart + ysize, zstart + zsize]

    # TODO: Switch to using a class for the bounding box
    # min_coord = Coordinate(x=xstart, y=ystart, z=zstart)
    # max_coord = Coordinate(x=xstart + xsize, y=ystart + ysize, z=zstart + zsize)

    return min_coord + max_coord



def findCentroid(mask:sitk.Image) -> np.ndarray:
    """Find the centroid of a region of interest (ROI) in a given binary mask image.

    Parameters
    ----------
    mask : sitk.Image
        Mask image to find the centroid within.

    Returns
    -------
    centroid : np.ndarray
        Numpy array containing the coordinates of the ROI centroid.
    """
    # Convert the mask to a uint8 image
    mask_uint = sitk.Cast(mask, sitk.sitkUInt8)
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(mask_uint)
    # Get the centroid coordinates as a physical point in the mask
    centroid_coords = stats.GetCentroid(1)
    # Convert the physical point to an index in the mask array
    centroid_idx = mask.TransformPhysicalPointToIndex(centroid_coords)
    return np.asarray(centroid_idx, dtype=np.float32)



def cropToCentroid(image:sitk.Image,
                   centroid:tuple,
                   crop_dimensions:tuple,
                   ) -> sitk.Image:
    """Crop an image centered on the centroid with specified crop dimension. No resizing/resampling is performed.

    Parameters
    ----------
    image : sitk.Image
        Image to crop.
    centroid : tuple
        Tuple of integers representing the centroid of the image to crop. Must have the same number of dimensions as the image.
    crop_dimensions : tuple
        Tuple of integers representing the dimensions to crop the image to. Must have the same number of dimensions as the image.

    Returns
    -------
    cropped_image : sitk.Image
        Cropped image.
    """
    # Check that the number of dimensions in the crop dimensions matches the number of dimensions in the image
    validateNewDimensions(image, crop_dimensions)

    # Check that the centroid dimensions match the image dimensions
    validateNewDimensions(image, centroid)

    min_x = int(centroid[0] - crop_dimensions[0] // 2)
    max_x = int(centroid[0] + crop_dimensions[0] // 2)
    min_y = int(centroid[1] - crop_dimensions[1] // 2)
    max_y = int(centroid[1] + crop_dimensions[1] // 2)
    min_z = int(centroid[2] - crop_dimensions[2] // 2)
    max_z = int(centroid[2] + crop_dimensions[2] // 2)


    img_x, img_y, img_z = image.GetSize()


    if min_x < 0:
        min_x, max_x = 0, crop_dimensions[0]
    elif max_x > img_x:
        min_x, max_x = img_x - crop_dimensions[0], img_x

    if min_y < 0:
        min_y, max_y = 0, crop_dimensions[1]
    elif max_y > img_y:
        min_y, max_y = img_y - crop_dimensions[1], img_y

    if min_z < 0:
        min_z, max_z = 0, crop_dimensions[2]
    elif max_z > img_z:
        min_z, max_z = img_z - crop_dimensions[2], img_z

    return image[min_x:max_x, min_y:max_y, min_z:max_z]

