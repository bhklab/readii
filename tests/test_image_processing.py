from yarea.loaders import *
from yarea.image_processing import *
import pytest

@pytest.fixture
def nsclcCTImage():
    nsclcCTPath = "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"
    return loadDicomSITK(nsclcCTPath)

@pytest.fixture
def nsclcSEGImage():
    nsclcSEGPath = "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/1000.000000-3D_Slicer_segmentation_result-67652/1-1.dcm"
    segDictionary = loadSegmentation(nsclcSEGPath, modality = 'SEG')
    return segDictionary['Heart']

def test_flattenImage(nsclcSEGImage):
    """Test removing extra dimension of image that has size 1"""
    actual = flattenImage(nsclcSEGImage)
    assert isinstance(actual, sitk.Image), \
        "Wrong object type, need to convert back to sitk.Image"
    assert actual.GetSize() == (512, 512, 304), \
        "Wrong image size"


def test_alignImages(nsclcCTImage, nsclcSEGImage):
    """Test setting segmentation origin, direction, and spacing to match the CT after flattening"""
    flattenedSEG = flattenImage(nsclcSEGImage)
    actual = alignImages(nsclcCTImage, flattenedSEG)
    assert actual.GetSize() == (512, 512, 304), \
        "Wrong image size"
    assert actual.GetSpacing() == (0.693359375, 0.693359375, 1.0), \
        "Wrong spacing"
    assert actual.GetOrigin() == (-182.1533203125, -314.1533203125, -305.0), \
        "Wrong origin"
