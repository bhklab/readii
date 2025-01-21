import pytest
import SimpleITK as sitk

from readii.image_processing import loadDicomSITK, loadSegmentation
from readii.process.images.crop import (
    apply_bounding_box_limits,
    check_bounding_box_single_dimension,
    crop_image_to_mask,
    crop_to_bounding_box,
    crop_to_centroid,
    crop_to_maxdim_cube,
    find_bounding_box,
    find_centroid,
    validate_new_dimensions,
)


@pytest.fixture
def nsclcCT():
    return "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"


@pytest.fixture
def nsclcSEG():
    return "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/1000.000000-3D_Slicer_segmentation_result-67652/1-1.dcm"


@pytest.fixture
def lung4D_ct_path():
    return "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"


@pytest.fixture
def lung4D_rt_path():
    return "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm"


@pytest.fixture
def lung4D_image(lung4D_ct_path):
    return loadDicomSITK(lung4D_ct_path)


@pytest.fixture
def lung4D_mask(lung4D_ct_path, lung4D_rt_path):
    segDictionary = loadSegmentation(
        lung4D_rt_path,
        modality="RTSTRUCT",
        baseImageDirPath=lung4D_ct_path,
        roiNames="Tumor_c.*",
    )
    return segDictionary["Tumor_c40"]


@pytest.mark.parametrize(
    "crop_method, expected_size",
    [
        ("bbox", (50, 50, 50)),
        ("centroid", (50, 50, 50)),
        ("cube", (50, 50, 50)),
        # ("pyradiomics", (22, 28, 14)),
    ],
)
def test_crop_image_to_mask_methods(
    lung4D_image,
    lung4D_mask,
    crop_method,
    expected_size,
    resize_dimensions=(50, 50, 50),
):
    """Test cropping image to mask with different methods"""
    cropped_image, cropped_mask = crop_image_to_mask(
        lung4D_image,
        lung4D_mask,
        crop_method,
        resize_dimensions,
    )
    assert (
        cropped_image.GetSize() == expected_size
    ), f"Cropped image size is incorrect, expected {expected_size}, got {cropped_image.GetSize()}"
    assert (
        cropped_mask.GetSize() == expected_size
    ), f"Cropped mask size is incorrect, expected {expected_size}, got {cropped_mask.GetSize()}"


####################################################################################################
# Parameterized tests for find_centroid and find_bounding_box


@pytest.fixture
def image_and_mask_with_roi(request, label_value: int = 1):
    """
    Fixture to create a 3D image and mask with a specified region of interest (ROI).

    This fixture is used indirectly in parameterized tests via the `indirect` keyword
    in `pytest.mark.parametrize`. The `request.param` provides the ROI coordinates, which
    are used to define the region of interest in the mask. The ROI is specified as a
    6-tuple (x_min, x_max, y_min, y_max, z_min, z_max).

    """
    # Create a 3D image
    image = sitk.Image(100, 100, 100, sitk.sitkInt16)
    mask = sitk.Image(100, 100, 100, sitk.sitkUInt8)

    # Unpack ROI from the request parameter and apply it to the mask
    roi = request.param
    mask[roi[0] : roi[1], roi[2] : roi[3], roi[4] : roi[5]] = label_value

    return image, mask


def test_find_bounding_box_and_centroid_bad_label():
    mask = sitk.Image(100, 100, 100, sitk.sitkUInt8)
    mask[10:20, 10:20, 10:20] = 2

    with pytest.raises(RuntimeError):
        find_bounding_box(mask)

    with pytest.raises(RuntimeError):
        find_centroid(mask)


# Test cases for find_bounding_box


@pytest.mark.parametrize(
    # First parameter passed indirectly via the fixture
    # Second parameter is the expected bounding box
    "image_and_mask_with_roi, expected_bbox",
    [
        #
        # x_min, x_max, y_min, y_max, z_min, z_max
        #
        # Simple case: Perfect bounding box
        ((85, 95, 70, 90, 60, 90), (85, 95, 70, 90, 60, 90)),
        # Complex case: Non-standard bounding box dimensions
        ((32, 68, 53, 77, 10, 48), (32, 68, 53, 77, 10, 48)),
        # Single-plane ROI: ROI in only one slice
        # since min_dim_size is 4, the ROI is expanded to 4 in if a side is too small
        # x_max is expanded to 24
        ((20, 21, 30, 60, 40, 80), (20, 24, 30, 60, 40, 80)),
        # Minimum size ROI
        # x_max is expanded to 49, y_max is expanded to 14, z_max is expanded to 9
        ((45, 46, 10, 12, 5, 6), (45, 49, 10, 14, 5, 9)),
    ],
    indirect=["image_and_mask_with_roi"],  # Use the fixture indirectly
)
def test_find_bounding_box(image_and_mask_with_roi, expected_bbox):
    _, mask = image_and_mask_with_roi
    bounding_box = find_bounding_box(mask, min_dim_size=4)
    assert (
        bounding_box == expected_bbox
    ), f"Bounding box is incorrect, expected {expected_bbox}, got {bounding_box}"


# Test cases for find_centroid


@pytest.mark.parametrize(
    "image_and_mask_with_roi, expected_centroid",
    [
        # Simple case: Perfect centroid
        ((85, 95, 70, 90, 60, 90), (90, 80, 75)),
        # Complex case: Non-standard dimensions
        ((32, 68, 53, 77, 10, 48), (50, 65, 29)),
        # Single-plane ROI
        ((20, 21, 30, 60, 40, 80), (20, 45, 60)),
        # Minimum size ROI
        ((45, 46, 10, 12, 5, 6), (45, 11, 5)),
    ],
    indirect=["image_and_mask_with_roi"],  # Use the fixture indirectly
)
def test_find_centroid(image_and_mask_with_roi, expected_centroid):
    _, mask = image_and_mask_with_roi
    centroid = find_centroid(mask)
    assert (
        centroid == expected_centroid
    ), f"Centroid is incorrect, expected {expected_centroid}, got {centroid}"
