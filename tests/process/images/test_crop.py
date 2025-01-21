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
    resize_image,
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
    lung4D_image, lung4D_mask, crop_method, expected_size, resize_dimensions=(50, 50, 50)
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


@pytest.fixture
def complex_image_and_mask():
    # The image and image are a 3D image with size 100x100x100
    # however, the ROI in the mask is 10x20x30

    image = sitk.Image(100, 100, 100, sitk.sitkInt16)
    mask = sitk.Image(100, 100, 100, sitk.sitkUInt8)

    mask[85:95, 70:90, 60:90] = 1

    return image, mask


@pytest.mark.parametrize(
    "crop_method",
    [
        "bbox",
        "centroid",
        "cube",
        # "pyradiomics",
    ],
)
@pytest.mark.parametrize(
    "resize_dimensions, expected_size",
    [
        ((50, 50, 50), (50, 50, 50)),
        ((100, 100, 100), (100, 100, 100)),
        ((200, 200, 200), (200, 200, 200)), # this only fails for centroid
    ],
)
def test_crop_image_to_mask_methods_complex(
    complex_image_and_mask, crop_method, resize_dimensions, expected_size
):
    """Test cropping image to mask with different methods"""
    image, mask = complex_image_and_mask
    cropped_image, cropped_mask = crop_image_to_mask(
        image,
        mask,
        crop_method,
        resize_dimensions=resize_dimensions,
    )
    assert (
        cropped_image.GetSize() == expected_size
    ), f"Cropped image size is incorrect, expected {expected_size}, got {cropped_image.GetSize()}"
    assert (
        cropped_mask.GetSize() == expected_size
    ), f"Cropped mask size is incorrect, expected {expected_size}, got {cropped_mask.GetSize()}"
