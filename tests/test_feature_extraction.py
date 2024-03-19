from readii.loaders import (
    loadDicomSITK, 
    loadRTSTRUCTSITK, 
    loadSegmentation,
) 

from readii.feature_extraction import (
    singleRadiomicFeatureExtraction,
    radiomicFeatureExtraction,
)

import pytest
import collections
import pandas as pd
import os 

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
def lung4DCTImage():
    lung4DCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"
    return loadDicomSITK(lung4DCTPath)

@pytest.fixture
def lung4DRTSTRUCTImage():
    lung4DRTSTRUCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm"
    lung4DCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"
    segDictionary = loadSegmentation(lung4DRTSTRUCTPath, modality = 'RTSTRUCT',
                                     baseImageDirPath = lung4DCTPath, roiNames = 'Tumor_c.*')
    return segDictionary['Tumor_c40']

@pytest.fixture
def pyradiomicsParamFilePath():
    return "src/readii/data/default_pyradiomics.yaml"

@pytest.fixture
def nsclcMetadataPath():
    return "tests/output/ct_to_seg_match_list_NSCLC_Radiogenomics.csv"


def test_singleRadiomicFeatureExtraction_SEG(nsclcCTImage, nsclcSEGImage, pyradiomicsParamFilePath):
    """Test single image feature extraction with a CT and SEG"""

    actual = singleRadiomicFeatureExtraction(nsclcCTImage, nsclcSEGImage, pyradiomicsParamFilePath)
    assert type(actual) == collections.OrderedDict, \
        "Wrong return type, expect a collections.OrderedDict"
    assert len(actual) == 1353, \
        "Wrong return size, check pyradiomics parameter file is correct"
    assert actual['diagnostics_Configuration_Settings']['label'] == 255, \
        "Wrong label getting passed for ROI"
    assert actual['diagnostics_Image-original_Size'] == (26, 21, 20), \
        "Cropped CT image is incorrect size"
    assert actual['diagnostics_Mask-original_Size'] == (26, 21, 20), \
        "Cropped segmentation mask is incorrect size"
    assert actual['diagnostics_Mask-original_Size'] == actual['diagnostics_Image-original_Size'], \
        "Cropped CT and segmentation mask dimensions do not match"
    assert actual['original_shape_MeshVolume'].tolist()== pytest.approx(1273.7916666666667), \
        "Volume feature is incorrect"


def test_singleRadiomicFeatureExtraction_RTSTRUCT(lung4DCTImage, lung4DRTSTRUCTImage, pyradiomicsParamFilePath):
    """Test single image feature extraction with a CT and RTSTRUCT"""

    actual = singleRadiomicFeatureExtraction(lung4DCTImage, lung4DRTSTRUCTImage, pyradiomicsParamFilePath)
    assert type(actual) == collections.OrderedDict, \
        "Wrong return type, expect a collections.OrderedDict"
    assert len(actual) == 1353, \
        "Wrong return size, check pyradiomics parameter file is correct"
    assert actual['diagnostics_Configuration_Settings']['label'] == 1, \
        "Wrong label getting passed for ROI"
    assert actual['diagnostics_Image-original_Size'] == (51, 92, 28), \
        "Cropped CT image is incorrect size"
    assert actual['diagnostics_Mask-original_Size'] == (51, 92, 28), \
        "Cropped segmentation mask is incorrect size"
    assert actual['diagnostics_Mask-original_Size'] == actual['diagnostics_Image-original_Size'], \
        "Cropped CT and segmentation mask dimensions do not match"
    assert actual['original_shape_MeshVolume'].tolist()== pytest.approx(66346.66666666667), \
        "Volume feature is incorrect"


def test_radiomicFeatureExtraction(nsclcMetadataPath):
    """Test full radiomicFeatureExtraction function with CT and SEG and default PyRadiomics 
       parameter file and no output"""
    
    actual = radiomicFeatureExtraction(nsclcMetadataPath,
                                       imageDirPath="tests/",
                                       roiNames = None)
    assert type(actual) == pd.core.frame.DataFrame, \
        "Wrong return type, expect a pandas DataFrame"
    assert actual.shape[1] == 1365, \
        "Wrong return size, should include image metadata, diagnostics, and pyradiomics features"
    assert actual['diagnostics_Configuration_Settings'][0]['label'] == 255, \
        "Wrong label getting passed for ROI"
    assert actual['diagnostics_Image-original_Size'][0] == (26, 21, 20), \
        "Cropped CT image is incorrect size"
    assert actual['diagnostics_Mask-original_Size'][0] == (26, 21, 20), \
        "Cropped segmentation mask is incorrect size"
    assert actual['original_shape_MeshVolume'][0].tolist()== pytest.approx(1273.7916666666667), \
        "Volume feature is incorrect"


def test_radiomicFeatureExtraction_output(nsclcMetadataPath):
    """Test output creation from radiomic feature extraction"""
    actual = radiomicFeatureExtraction(nsclcMetadataPath,
                                       imageDirPath = "tests/",
                                       roiNames = None,
                                       outputDirPath = "tests/output/")
    assert os.path.exists("tests/output/features/radiomicfeatures_NSCLC_Radiogenomics.csv")