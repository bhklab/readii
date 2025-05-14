import pytest
import SimpleITK as sitk

from readii.image_processing import loadDicomSITK, loadSegmentation
from readii.process.images.crop import (
    crop_and_resize_image_and_mask
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
        roiNames=["Tumor_c40"],
    )
    return segDictionary["Tumor_c40"]


def test_default_crop_and_resize_image(lung4D_image, lung4D_mask):
    expected_size = (93, 93, 93)
    cropped_image, cropped_mask = crop_and_resize_image_and_mask(lung4D_image, lung4D_mask)
    assert cropped_image.GetSize() == expected_size, \
        f"Cropped image size is incorrect, expected {expected_size}, got {cropped_image.GetSize()}"
    assert cropped_mask.GetSize() == expected_size, \
        f"Cropped mask size is incorrect, expected {expected_size}, got {cropped_mask.GetSize()}"

@pytest.mark.parametrize(
    "crop_method, resize_dimension, expected_size",
    [
        # No resizing
        ("bounding_box", None, (52, 93, 28)),
        ("centroid", None, (50, 50, 50)),
        ("cube", None, (93, 93, 93)),
        # Resize down to 50x50x50
        ("bounding_box", 50, (50, 50, 50)),
        ("centroid", 50, (50, 50, 50)),
        ("cube", 50, (50, 50, 50)),
        # Resize to odd value
        ("bounding_box", 49, (49, 49, 49)),
        ("centroid", 49, (49, 49, 49)),
        ("cube", 49, (49, 49, 49)),
        # Resize up to 98x98x98
        ("bounding_box", 98, (98, 98, 98)),
        ("centroid", 98, (98, 98, 98)),
        ("cube", 98, (98, 98, 98)),
    ],
)
def test_crop_and_resize_image_and_mask_methods_and_resize_dimension(
    lung4D_image,
    lung4D_mask,
    crop_method,
    resize_dimension,
    expected_size,
):
    """Test cropping image to mask with different methods"""
    cropped_image, cropped_mask = crop_and_resize_image_and_mask(
        lung4D_image,
        lung4D_mask,
        crop_method = crop_method,
        resize_dimension = resize_dimension,
    )
    assert (
        cropped_image.GetSize() == expected_size
    ), f"Cropped image size is incorrect, expected {expected_size}, got {cropped_image.GetSize()}"
    assert (
        cropped_mask.GetSize() == expected_size
    ), f"Cropped mask size is incorrect, expected {expected_size}, got {cropped_mask.GetSize()}"


