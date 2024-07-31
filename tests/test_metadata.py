import pytest
import os

from readii.metadata import (
    matchCTtoSegmentation,
    getSegmentationType,
    saveDataframeCSV,
    getCTWithSegmentation
)

@pytest.fixture
def nsclcSummaryFilePath():
    return "tests/.imgtools/imgtools_NSCLC_Radiogenomics.csv"

@pytest.fixture
def lung4DSummaryFilePath():
    return "tests/.imgtools/imgtools_4D-Lung.csv"

@pytest.fixture
def lung4DEdgesSummaryFilePath():
    return "tests/.imgtools/imgtools_4D-Lung_edges.csv"


def test_matchCTtoSEG(nsclcSummaryFilePath):
    """Test generating matched summary file for CT and DICOM SEG"""
    actual = matchCTtoSegmentation(nsclcSummaryFilePath, 
                                   segType = "SEG")
    assert len(actual) == 1, \
        "Incorrect merge, should result in only 1 row"
    assert actual['reference_ct_seg'][0] == '1.3.6.1.4.1.14519.5.2.1.4334.1501.312037286778380630549945195741', \
        "The segmentation's reference CT ID is wrong/missing"
    assert actual['reference_ct_seg'][0] == actual['series_CT'][0], \
        "Segmentation reference ID does not match CT series ID"
    assert actual['modality_seg'][0] == 'SEG', \
        "Incorrect segmentation type has been found"


def test_matchCTtoRTSTRUCT(lung4DSummaryFilePath):
    """Test generating matched summary file for CT and RTSTRUCT"""
    actual = matchCTtoSegmentation(lung4DSummaryFilePath, 
                                   segType = "RTSTRUCT")
    assert len(actual) == 1, \
        "Incorrect merge, should result in only 1 row"
    assert actual['reference_ct_seg'][0] == '1.3.6.1.4.1.14519.5.2.1.6834.5010.339023390306606021995936229543', \
        "The segmentation's reference CT ID is wrong/missing"
    assert actual['reference_ct_seg'][0] == actual['series_CT'][0], \
        "Segmentation reference ID does not match CT series ID"
    assert actual['modality_seg'][0] == 'RTSTRUCT', \
        "Incorrect segmentation type has been found"


def test_matchCTtoSegmentation_output(nsclcSummaryFilePath):
    """Test saving output of summary file"""
    actual = matchCTtoSegmentation(nsclcSummaryFilePath, 
                                   segType = "SEG",
                                   outputFilePath = "tests/output/ct_to_seg_match_list_NSCLC_Radiogenomics.csv")
    assert os.path.exists("tests/output/ct_to_seg_match_list_NSCLC_Radiogenomics.csv") == True, \
        "Output does not exist, double check output file is named correctly."


def test_getCTWithRTTRUCT(lung4DEdgesSummaryFilePath):
    """Test getting CTs with RTSTRUCT segmentation from edges file"""
    actual = getCTWithSegmentation(lung4DEdgesSummaryFilePath, 
                                   segType = "RTSTRUCT")
    assert len(actual) == 1, \
        "Incorrect merge, should result in only 1 row"
    assert actual['reference_ct_seg'][0] == '1.3.6.1.4.1.14519.5.2.1.6834.5010.339023390306606021995936229543', \
        "The segmentation's reference CT ID is wrong/missing"
    assert actual['reference_ct_seg'][0] == actual['series_CT'][0], \
        "Segmentation reference ID does not match CT series ID"
    assert actual['modality_seg'][0] == 'RTSTRUCT', \
        "Incorrect segmentation type has been found"


def test_getCTtoSegmentation_output(lung4DEdgesSummaryFilePath):
    """Test saving output of summary file"""
    actual = getCTWithSegmentation(lung4DEdgesSummaryFilePath, 
                                   segType = "RTSTRUCT",
                                   outputFilePath = "tests/output/ct_to_seg_match_list_4D-Lung.csv")
    assert os.path.exists("tests/output/ct_to_seg_match_list_4D-Lung.csv") == True, \
        "Output does not exist, double check output file is named correctly."


@pytest.mark.parametrize(
    "wrongSeg",
    [
        'CT',
        'Nonsense',
        ""
    ]
)
def test_matchCTtoSegmentation_error(nsclcSummaryFilePath, wrongSeg):
    """Check ValueError is raised when incorrect segType is passed"""
    with pytest.raises(ValueError):
        matchCTtoSegmentation(nsclcSummaryFilePath,
                              segType = wrongSeg)


def test_saveDataframeCSV_outputFilePath_error(nsclcSummaryFilePath):
    """Check ValueError is raised when incorrect outputFilePath is passed"""
    testDataframe = matchCTtoSegmentation(nsclcSummaryFilePath, 
                                   segType = "SEG")
    badFilePath = "notacsv.xlsx"
    with pytest.raises(ValueError):
        saveDataframeCSV(testDataframe, badFilePath)

@pytest.mark.parametrize(
    "wrongSeg",
    [
        'CT',
        'Nonsense',
        ""
    ]
)
def test_getCTWithRTSTRUCT_error(lung4DEdgesSummaryFilePath, wrongSeg):
    """Check ValueError is raised when incorrect segType is passed"""
    with pytest.raises(ValueError):
        getCTWithSegmentation(lung4DEdgesSummaryFilePath, 
                                   segType = wrongSeg)

def test_getCTWithSEG_error(nsclcSummaryFilePath):
    """Check ValueError is raised when incorrect segType is passed"""
    with pytest.raises(ValueError):
        getCTWithSegmentation(nsclcSummaryFilePath, 
                                   segType = "SEG")


@pytest.mark.parametrize(
    "notADataFrame",
    [
        ['list', 'of', 'features'],
        "Just a string",
        {"feat1": 34, "feat2": 10000, "feat3": 3.141592}
    ]
)
def test_saveDataframeCSV_dataframe_error(notADataFrame):
    """Check ValueError is raised when something other than pd.DataFrame is passed"""
    goodFilePath = "tests/output/badDataframeExample.csv"
    with pytest.raises(ValueError):
        saveDataframeCSV(notADataFrame, goodFilePath)


def test_getSegmentationType_SEG(nsclcSummaryFilePath):
    """Test getting segmentation type from summary file with SEG and CT"""
    actual = getSegmentationType(nsclcSummaryFilePath)
    assert actual == "SEG", \
        "Wrong segmentation type found"


def test_getSegmentationType_RTSTRUCT(lung4DSummaryFilePath):
    """Test getting segmentation type from summary file with RTSTRUCT and CT"""
    actual = getSegmentationType(lung4DSummaryFilePath)
    assert actual == "RTSTRUCT", \
        "Wrong segmentation type found"


@pytest.mark.parametrize(
    "notACSV",
    [
        "tests/.imgtools/imgtools_NSCLC_Radiogenomics.json",
        "Just a string",
        "tests/.imgtools/imgtools_4D-Lung.json"
    ]
)
def test_getSegmentation_dataframe_error(notACSV):
    """Check ValueError is raised when something other than a csv file is passed"""
    with pytest.raises(ValueError):
        getSegmentationType(notACSV)
