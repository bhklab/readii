from typing import Literal

import SimpleITK as sitk
from imgtools.coretypes.box import RegionBox
from imgtools.transforms.functional import resize

from readii.utils import logger

CropMethods = Literal["bounding_box", "centroid", "cube"]


def crop_and_resize_image_and_mask(image: sitk.Image,
                                   mask: sitk.Image,
                                   label: int = 1,
                                   crop_method: CropMethods = "cube",
                                   resize_dimension: int | None = None
                                  ) -> tuple[sitk.Image, sitk.Image]:
    """Crop an image and mask to an ROI in the mask and resize to a specified crop dimensions.

    Parameters
    ----------
    image : sitk.Image
        Image to crop.
    mask : sitk.Image
        Mask to crop the image to. Will also be cropped.
    label : int, default 1
        Voxel value of the region of interest to crop to in the mask. Set to 1 by default.
    crop_method : str, default "cube"
        Method to use to crop the image to the mask. Must be one of "bounding_box", "centroid", "cube".
    resize_dimensions : int, optional
        Dimension to resize the image to. Will apply this value in all dimensions, so result will be a cube.
    
    Returns
    -------
    cropped_image : sitk.Image
        Cropped image.
    cropped_mask : sitk.Image
        Cropped mask.

    Notes
    -----
    The bounding box is generated as a `RegionBox` object from `med-imagetools`.

    For the `centroid` method, `resize_dimension` is used to generate a cube around the centroid of the mask.
    If `resize_dimension` is not provided, it defaults to 50 voxels.

    For the `cube` method, the bounding box is expanded to a cube with the maximum region of interest dimension.

    If `resize_dimension` is provided, the cropped image and mask are resized to the specified dimensions
    using `imgtools.ops.functional.resize` with linear interpolation.
    """
    # Check that the provided label is present in the mask
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(mask)
    if label not in stats.GetLabels():
        msg = f"Label {label} not present in mask. Must be one of {stats.GetLabels()}"
        logger.exception(msg)
        raise ValueError(msg)

    # Generate bounding box based on the specified crop method
    match crop_method:
        case "bounding_box":
            # Generate a bounding box around a mask
            crop_box = RegionBox.from_mask_bbox(mask, label)
        
        case "centroid":
            if resize_dimension is None:
                # Set resize_dimension to 50 if not provided -> default expected dimension for FMCIB
                resize_dimension = 50

            # Generate a cube bounding box with resize_dimensions around the centroid of a mask
            crop_box = RegionBox.from_mask_centroid(mask, label).expand_to_cube(resize_dimension)
        
        case "cube":
            # Generate a bounding box around the mask, then expand the dimensions to a cube with the maximum bounding box dimension
            crop_box = RegionBox.from_mask_bbox(mask, label)
            crop_box = crop_box.expand_to_cube(max(crop_box.size))
        
        case _:
            msg = f"Invalid crop method: {crop_method}. Must be one of 'bounding_box', 'centroid', or 'cube'."
            raise ValueError(msg)

    # Crop the image and mask to the bounding box
    cropped_image, cropped_mask = crop_box.crop_image_and_mask(image, mask)

    if resize_dimension is not None:
        # Resize and resample the cropped image with linear interpolation to desired dimensions
        cropped_image = resize(cropped_image, size = resize_dimension, interpolation = 'linear')

        # Resize and resample the cropped mask with nearest neighbor interpolation to desired dimensions
        # This can end up being returned as a float32 image, so need to cast to uint8 to avoid issues with label values
        cropped_mask = resize(cropped_mask, size = resize_dimension, interpolation = 'nearest')

        # Cast the cropped mask to uint8 to avoid issues with label values
        cropped_mask = sitk.Cast(cropped_mask, sitk.sitkUInt8)

    return cropped_image, cropped_mask


if __name__ == "__main__":
    from imgtools.io import read_dicom_auto
    from rich import print as rprint

    from readii.loaders import loadRTSTRUCTSITK

    image = read_dicom_auto("tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543")

    rois = loadRTSTRUCTSITK(rtstructPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm",
                            baseImageDirPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543",
                            roiNames = "Tumor_c.*")

    rprint("Original image size:", image.GetSize())

    mask = rois["Tumor_c40"]

    bbox_image, bbox_mask = crop_and_resize_image_and_mask(image, mask, crop_method = "bounding_box")
    rprint(f"Bounding box: {bbox_image.GetSize()}")
    rprint(f"Bounding box mask: {bbox_mask.GetSize()}")

    centroid_image, centroid_mask = crop_and_resize_image_and_mask(image, mask, crop_method = "centroid")
    rprint(f"Centroid: {centroid_image.GetSize()}")
    rprint(f"Centroid mask: {centroid_mask.GetSize()}")

    cube_image, cube_mask = crop_and_resize_image_and_mask(image, mask, crop_method = "cube")
    rprint(f"Cube: {cube_image.GetSize()}")
    rprint(f"Cube mask: {cube_mask.GetSize()}")