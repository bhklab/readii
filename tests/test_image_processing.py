from readii.loaders import *
from readii.image_processing import *
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

@pytest.fixture
def lung4DRTSTRUCTImage():
    lung4DRTSTRUCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm"
    lung4DCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"
    segDictionary = loadSegmentation(lung4DRTSTRUCTPath, modality = 'RTSTRUCT',
                                     baseImageDirPath = lung4DCTPath, roiNames = ['Tumor_c40'])
    return segDictionary['Tumor_c40']


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

@pytest.mark.parametrize(
    "segImage, expected",
    [
        ("nsclcSEGImage", 255),
        ("lung4DRTSTRUCTImage", 1)
    ]
)
def test_getROIVoxelLabel(segImage, expected, request):
    """Test getting the voxel value in the ROI in a segmentation for both SEG and RTSTRUCT images"""
    segImage = request.getfixturevalue(segImage)
    assert getROIVoxelLabel(segImage) == expected

@pytest.mark.parametrize(
    "segImage, expected",
    [
        ("nsclcSEGImage", (238, 252, 124)),
        ("lung4DRTSTRUCTImage", (63, 312, 328))
    ]
)
def test_getROICenterCoords(segImage, expected, request):
    """Test getting the center slice and coordinates for an ROI in both SEG and RTSTRUCT images"""
    segImage = request.getfixturevalue(segImage)
    flatSegImage = flattenImage(segImage)
    centerSliceIdx, centerColumnPixelIdx, centerRowPixelIdx = getROICenterCoords(flatSegImage)
    assert centerSliceIdx == expected[0], \
        "Slice number is wrong"
    assert centerColumnPixelIdx == expected[1], \
        "Center column pixel value is wrong"
    assert centerRowPixelIdx == expected[2], \
        "Center row pixel value is wrong"