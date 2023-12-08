from yarea.loaders import *

@pytest.fixture
def nsclcCTPath():
    return "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"

@pytest.fixture
def nsclcSEGPath():
    return "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/1000.000000-3D_Slicer_segmentation_result-67652/1-1.dcm"

@pytest.fixture
def lung4DCTPath():
    return "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"

@pytest.fixture
def lung4DRTSTRUCTPath():
    return "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm"


def test_loadDicomSITK(nsclcCTPath):
    """Test loading DICOM from directory."""
    actual = loadDicomSITK(nsclcCTPath)
    assert isinstance(actual, sitk.Image), \
        "Wrong object type"
    assert actual.GetSize() == (512, 512, 304), \
        "Wrong image size"
    assert actual.GetSpacing() == (0.693359375, 0.693359375, 1.0), \
        "Wrong spacing"
    assert actual.GetOrigin() == (-182.1533203125, -314.1533203125, -305.0), \
        "Wrong origin"


def test_loadSegmentationSEG(nsclcSEGPath):
    """Test loading a DICOM SEG file"""
    actual = loadSegmentation(segImagePath = nsclcSEGPath,
                              modality = 'SEG')

    assert isinstance(actual, dict), \
        "Wrong object type, should be dictionary"
    assert list(actual.keys()) == ['Heart'], \
        "Segmentation label is wrong, should be Heart"

    actualImage = actual['Heart']

    assert isinstance(actualImage, sitk.Image), \
        "Wrong object type"
    assert actualImage.GetSize() == (512, 512, 304, 1), \
        "Wrong image size"
    assert actualImage.GetSpacing() == (0.693359375, 0.693359375, 1.0, 1.0), \
        "Wrong spacing"
    assert actualImage.GetOrigin() == (-182.1533203125, -314.1533203125, -305.0, 0.0), \
        "Wrong origin"


def test_loadSegmentationRTSTRUCT(lung4DRTSTRUCTPath, lung4DCTPath):
    """Test loading a RTSTRUCT file"""
    actual = loadSegmentation(segImagePath = lung4DRTSTRUCTPath,
                              modality = 'RTSTRUCT',
                              baseImageDirPath = lung4DCTPath,
                              roiNames = 'Tumor_c.*')

    assert isinstance(actual, dict), \
        "Wrong object type, should be dictionary"
    assert list(actual.keys()) == ['Tumor_c40'], \
        "Segmentation label is wrong, should be Heart"
    
    actualImage = actual['Tumor_c40']

    assert isinstance(actualImage, sitk.Image), \
        "Wrong object type"
    assert actualImage.GetSize() == (512, 512, 99), \
        "Wrong image size"
    assert actualImage.GetSpacing() == (0.9766, 0.9766, 3.0), \
        "Wrong spacing"
    assert actualImage.GetOrigin() == (-250.0, -163.019, -1132.0), \
        "Wrong origin"


def test_loadSegmentation_error(nsclcSEGPath):
    """Check ValueError raised when wrong segmentation type is passed"""
    with pytest.raises(ValueError):
        loadSegmentation(segImagePath = nsclcSEGPath,
                         modality = 'CT')