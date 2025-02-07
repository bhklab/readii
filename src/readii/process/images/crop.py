from imgtools.coretypes.box import RegionBox
from imgtools.ops.functional import resize
from typing import Literal, Optional
import SimpleITK as sitk

CropMethods = Literal["bounding_box", "centroid", "cube", "pyradiomics"]


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
    resize_dimensions : tuple[int,int,int], optional
        Dimensions to resize the image to.
    
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

    # Generate bounding box based on the specified crop method
    match crop_method:
        case "bounding_box":
            # Generate a bounding box around a mask
            crop_box = RegionBox.from_mask_bbox(mask, label)
        
        case "centroid":
            if resize_dimension == None:
                # Set resize_dimension to 50 if not provided -> default expected dimension for FMCIB
                resize_dimension = 50
            
            # Generate a cube bounding box with resize_dimensions around the centroid of a mask
            crop_box = RegionBox.from_mask_centroid(mask, label).expand_to_cube(resize_dimension)
        
        case "cube":
            # Generate a bounding box around the mask, then expand the dimensions to a cube with the maximum bounding box dimension
            crop_box = RegionBox.from_mask_bbox(mask, label)
            crop_box = crop_box.expand_to_cube(max(crop_box.size))
        
        case _:
            msg = f"Invalid crop method: {crop_method}. Must be one of 'bounding_box', 'centroid', 'cube', or 'pyradiomics'."
            raise ValueError(msg)

    # Crop the image and mask to the bounding box
    cropped_image, cropped_mask = crop_box.crop_image_and_mask(image, mask)

    if resize_dimension is not None:
        # Resize and resample the cropped image and mask with linear interpolation to desired dimensions
        cropped_image = resize(cropped_image, size = resize_dimension)
        cropped_mask = resize(cropped_mask, size = resize_dimension)

    return cropped_image, cropped_mask


if __name__ == "__main__":
    from rich import print
    from imgtools.coretypes import Coordinate3D
    from imgtools.io import read_dicom_series
    from readii.loaders import loadRTSTRUCTSITK

    image = read_dicom_series("tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543")

    rois = loadRTSTRUCTSITK(rtstructPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm",
                            baseImageDirPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543",
                            roiNames = "Tumor_c.*")

    print(image.GetSize())

    mask = rois["Tumor_c40"]

    print(mask.GetSize())
    # bbox_image, bbox_mask = crop_and_resize_image_and_mask(image, mask, crop_method = "bounding_box")
    # print(f"Bounding box: {bbox_image.GetSize()}")
    # print(f"Bounding box mask: {bbox_mask.GetSize()}")

    # centroid_image, centroid_mask = crop_and_resize_image_and_mask(image, mask, crop_method = "centroid")
    # print(f"Centroid: {centroid_image.GetSize()}")
    # print(f"Centroid mask: {centroid_mask.GetSize()}")

    cube_image, cube_mask = crop_and_resize_image_and_mask(image, mask, crop_method = "cube")
    print(f"Cube: {cube_image.GetSize()}")
    print(f"Cube mask: {cube_mask.GetSize()}")