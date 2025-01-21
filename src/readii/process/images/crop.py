
from typing import Literal

import numpy as np
import SimpleITK as sitk
from imgtools.ops.functional import resize
from radiomics import imageoperations

from readii.image_processing import getROIVoxelLabel
from readii.utils import logger


def validate_new_dimensions(image:sitk.Image,
                            new_dimensions:tuple | int
                            ) -> None:
    """Validate that the input new dimensions are valid for the image.

    Parameters
    ----------
    image : sitk.Image
        Image to validate the new dimensions for.
    new_dimensions : tuple or int
        Tuple of values representing the new dimensions to validate, or a single integer representing the number of dimensions.

    Raises
    ------
    ValueError
        If the new dimensions are not valid for the image.
    """
    # Check that the number of dimensions in the new dimensions matches the number of dimensions in the image
    if isinstance(new_dimensions, tuple):
        if len(new_dimensions) != image.GetDimension():
            msg = f"Number of dimensions in new_dimensions ({len(new_dimensions)}) does not match the number of dimensions in the image ({image.GetDimension()})."
            logger.exception(msg)
            raise ValueError(msg)

    elif isinstance(new_dimensions, int):
        if new_dimensions != image.GetDimension():
            msg = f"Number of dimensions in new_dimensions ({new_dimensions}) does not match the number of dimensions in the image ({image.GetDimension()})."
            logger.exception(msg)
            raise ValueError(msg)
    
    else:
        msg = "New dimensions must be a tuple of integers or a single integer."
        logger.exception(msg)
        raise ValueError(msg)



def find_bounding_box(mask:sitk.Image,
                      min_dim_size:int = 4
                      ) -> tuple:
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

    
    # Calculate the maximum coordinate of the bounding box by adding the size to the starting coordinate
    xend, yend, zend = xstart + xsize, ystart + ysize, zstart + zsize

    # TODO: Switch to using a class for the bounding box
    # min_coord = Coordinate(x=xstart, y=ystart, z=zstart)
    # max_coord = Coordinate(x=xstart + xsize, y=ystart + ysize, z=zstart + zsize)

    return xstart, xend, ystart, yend, zstart, zend


def check_bounding_box_single_dimension(bb_min_val:int, 
                                        bb_max_val:int,
                                        expected_dim:int, 
                                        img_dim:int
                                        ) -> tuple[int,int]:
    """Check if minimum and maximum values for a single bounding box dimension fall within the same dimension in the image the bounding box was made for.
    
    Parameters
    ----------
    bb_min_val : int
        Minimum value for the bounding box dimension.
    bb_max_val : int
        Maximum value for the bounding box dimension.
    expected_dim : int
        Expected dimension of the bounding box.
    img_dim : int
        Dimension of the image the bounding box was made for.
    
    Returns
    -------
    bb_min_val : int
        Updated minimum value for the bounding box dimension.
    bb_max_val : int
        Updated maximum value for the bounding box dimension.

    Examples
    --------
    >>> check_bounding_box_single_dimension(0, 10, 20, 30)
    (0, 10)
    >>> check_bounding_box_single_dimension(30, 40, 10, 30)
    (20, 30)
    >>> check_bounding_box_single_dimension(bb_x_min, bb_x_max, expected_dim_x, img_dim_x)
    """
    # Check if the minimum bounding box value is outside the image
    if bb_min_val < 0:
        # Set the minimum value to 0 (edge of image) and the max value to the minimum of the expected dimension or edge of image
        bb_min_val, bb_max_val = 0, min(expected_dim, img_dim)
    
    # Check if the maximum bounding box value is outside the image
    if bb_max_val > img_dim:
        # Set the minimum value to the maximum of the image dimension or edge of image and the max value to the edge of image
        bb_min_val, bb_max_val = max(0, img_dim - expected_dim), img_dim

    return bb_min_val, bb_max_val



def apply_bounding_box_limits(image:sitk.Image,
                              bounding_box:tuple[int,int,int,int,int,int],
                              expected_dimensions:tuple[int,int,int]
                              ) -> tuple:
    """Check that bounding box coordinates are within the image dimensions. If not, move bounding box to the edge of the image and expand to expected dimension.
    
    Parameters
    ----------
    image : sitk.Image
        Image to check the bounding box coordinates against.
    bounding_box : tuple[int,int,int,int,int,int]
        Bounding box to check the coordinates of.
    expected_dimensions : tuple[int,int,int]
        Expected dimensions of the bounding box. Used if the bounding box needs to be shifted to the edge of the image.
    
    Returns
    -------
    min_x, min_y, min_z, max_x, max_y, max_z : tuple[int,int,int,int,int,int]
        Updated bounding box coordinates.
    """
    # Get the size of the image to use to determine if crop dimensions are larger than the image
    img_x, img_y, img_z = image.GetSize()

    # Extract the bounding box coordinates
    min_x, max_x, min_y, max_y, min_z, max_z = bounding_box

    # Check each bounding box dimensions coordinates and move to image edge if not within image
    min_x, max_x = check_bounding_box_single_dimension(min_x, max_x, expected_dimensions[0], img_x)
    min_y, max_y = check_bounding_box_single_dimension(min_y, max_y, expected_dimensions[1], img_y)
    min_z, max_z = check_bounding_box_single_dimension(min_z, max_z, expected_dimensions[2], img_z)

    return min_x, max_x, min_y, max_y, min_z, max_z



def find_centroid(mask:sitk.Image) -> np.ndarray:
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
    return centroid_idx



def crop_to_centroid(image:sitk.Image,
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
    validate_new_dimensions(image, crop_dimensions)

    # Check that the centroid dimensions match the image dimensions
    validate_new_dimensions(image, centroid)

    min_x = int(centroid[0] - crop_dimensions[0] // 2)
    max_x = int(centroid[0] + crop_dimensions[0] // 2)
    min_y = int(centroid[1] - crop_dimensions[1] // 2)
    max_y = int(centroid[1] + crop_dimensions[1] // 2)
    min_z = int(centroid[2] - crop_dimensions[2] // 2)
    max_z = int(centroid[2] + crop_dimensions[2] // 2)

    # Test if bounding box coordinates are within the image, move to image edge if not
    min_x, max_x, min_y, max_y, min_z, max_z = apply_bounding_box_limits(image, 
                                                                         bounding_box = [min_x, max_x, min_y, max_y, min_z, max_z],
                                                                         expected_dimensions = crop_dimensions)

    return image[min_x:max_x, min_y:max_y, min_z:max_z]



def crop_to_bounding_box(image:sitk.Image,
                         bounding_box:tuple[int,int,int,int,int,int],
                         resize_dimensions:tuple[int,int,int]
                         ) -> sitk.Image:
    """Crop an image to a given bounding box and resize to a specified crop dimensions.

    Parameters
    ----------
    image : sitk.Image
        Image to crop.
    bounding_box : tuple[int,int,int,int,int,int]
        Bounding box to crop the image to. The order is (min_x, min_y, min_z, max_x, max_y, max_z).
    resize_dimensions : tuple[int,int,int]
        Dimensions to resize the image to.
    
    Returns
    -------
    cropped_image : sitk.Image
        Cropped image.
    """
    # Check that the number of dimensions in the crop dimensions matches the number of dimensions in the image
    validate_new_dimensions(image, resize_dimensions)

    # Check that the number of bounding box dimensions match the image dimensions
    validate_new_dimensions(image, int(len(bounding_box)/2))

    # Get bounding box dimensions for limit testing
    bounding_box_dimensions = np.array(bounding_box[3:]) - np.array(bounding_box[:3])

    # Test if bounding box coordinates are within the image, move to image edge if not
    min_x, max_x, min_y, max_y, min_z, max_z = apply_bounding_box_limits(image, bounding_box, bounding_box_dimensions)

    # Crop image to the bounding box
    img_crop = image[min_x:max_x, min_y:max_y, min_z:max_z]
    # Resample the image to the new dimensions and spacing
    img_crop = resize(img_crop, size = resize_dimensions)
    return img_crop



def crop_to_maxdim_cube(image:sitk.Image,
                        bounding_box:tuple[int,int,int,int,int,int],
                        resize_dimensions:tuple[int,int,int]
                        ) -> sitk.Image:
    """
    Crop given image to a cube based on the max dim from a bounding box and resize to specified input size.

    Parameters
    ----------
    image : sitk.Image
        Image to crop.
    bounding_box : tuple[int,int,int,int,int,int]
        Bounding box to find maximum dimension from. The order is (min_x, min_y, min_z, max_x, max_y, max_z).
    resize_dimensions : tuple[int,int,int]
        Crop dimensions to resize the image to.

    Returns
    -------
        sitk.Image: The cropped and resized image.
    """
    # Check that the number of dimensions in the crop dimensions matches the number of dimensions in the image
    validate_new_dimensions(image, resize_dimensions)

    # Check that the number of bounding box dimensions match the image dimensions
    validate_new_dimensions(image, len(bounding_box)//2)

    # Extract out the bounding box coordinates
    min_x, max_x, min_y, max_y, min_z, max_z = bounding_box

    # Get maximum dimension of bounding box
    max_dim = max(max_x - min_x, max_y - min_y, max_z - min_z)
    mean_x = int((max_x + min_x) // 2)
    mean_y = int((max_y + min_y) // 2)
    mean_z = int((max_z + min_z) // 2)

    # define new bounding boxes based on the maximum dimension of ROI bounding box
    min_x = int(mean_x - max_dim // 2)
    max_x = int(mean_x + max_dim // 2)
    min_y = int(mean_y - max_dim // 2)
    max_y = int(mean_y + max_dim // 2)
    min_z = int(mean_z - max_dim // 2)
    max_z = int(mean_z + max_dim // 2)

    # Test if bounding box coordinates are within the image, move to image edge if not
    min_x, max_x, min_y, max_y, min_z, max_z = apply_bounding_box_limits(image, 
                                                                         bounding_box = (min_x, max_x, min_y, max_y, min_z, max_z),
                                                                         expected_dimensions = [max_dim, max_dim, max_dim])
    # Crop image to the cube bounding box
    img_crop = image[min_x:max_x, min_y:max_y, min_z:max_z]
    # Resample the image to the new dimensions and spacing
    img_crop = resize(img_crop, size=resize_dimensions)
    return img_crop



def crop_with_pyradiomics(image:sitk.Image,
                          mask:sitk.Image,
                          mask_label:int = None
                          ) -> tuple[sitk.Image, sitk.Image]:
    """Crop an image to a bounding box around a region of interest in the mask using PyRadiomics functions.

    Parameters
    ----------
    image : sitk.Image
        Image to crop.
    mask : sitk.Image
        Mask to crop the image to.
    mask_label : int, optional
        Label of the region of interest to crop to in the mask. If not provided, will use the label of the first non-zero voxel in the mask.
    
    Returns
    -------
    image_crop : sitk.Image
        Cropped image.
    mask_crop : sitk.Image
        Cropped mask.
    """
    # Get the label of the region of interest in the mask if not provided
    if not mask_label:
        mask_label = getROIVoxelLabel(mask)
    
    # Check that CT and segmentation correspond, segmentationLabel is present, and dimensions match
    bounding_box, corrected_mask = imageoperations.checkMask(image, mask, label=mask_label)

    # Update the mask if correction was generated by checkMask
    if corrected_mask:
        mask = corrected_mask
    
    # Crop the image and mask to the bounding box
    image_crop, mask_crop = imageoperations.cropToTumorMask(image, mask, bounding_box)

    return image_crop, mask_crop



def crop_image_to_mask(image:sitk.Image,
                       mask:sitk.Image,
                       crop_method:Literal["bounding_box", "centroid", "cube", "pyradiomics"],
                       resize_dimensions:tuple[int,int,int]
                       ) -> tuple[sitk.Image, sitk.Image]:
    """Crop an image and mask to an ROI in the mask and resize to a specified crop dimensions.

    Parameters
    ----------
    image : sitk.Image
        Image to crop.
    mask : sitk.Image
        Mask to crop the image to. Will also be cropped.
    crop_method : str, optional
        Method to use to crop the image to the mask. Must be one of "bounding_box", "centroid", or "cube".
    resize_dimensions : tuple[int,int,int]
        Dimensions to resize the image to.
    
    Returns
    -------
    cropped_image : sitk.Image
        Cropped image.
    cropped_mask : sitk.Image
        Cropped mask.
    """
    match crop_method:
        case "bbox":
            bbox_coords = find_bounding_box(mask)
            cropped_image = crop_to_bounding_box(image, bbox_coords, resize_dimensions)
            cropped_mask = crop_to_bounding_box(mask, bbox_coords, resize_dimensions)
        
        case "centroid":
            centroid = find_centroid(mask)
            cropped_image = crop_to_centroid(image, centroid, resize_dimensions)
            cropped_mask = crop_to_centroid(mask, centroid, resize_dimensions)
        
        case "cube":
            bbox_coords = find_bounding_box(mask)
            cropped_image = crop_to_maxdim_cube(image, bbox_coords, resize_dimensions)
            cropped_mask = crop_to_maxdim_cube(mask, bbox_coords, resize_dimensions)
        
        case "pyradiomics":
            cropped_image, cropped_mask = crop_with_pyradiomics(image, mask)
        
        case _:
            msg = f"Invalid crop method: {crop_method}. Must be one of 'bbox', 'centroid', 'cube', or 'pyradiomics'."
            raise ValueError(msg)
    
    return cropped_image, cropped_mask