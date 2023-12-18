from yarea.metadata import *
import pytest

@pytest.fixture
def nsclcSummaryFilePath():
    return "tests/.imgtools/imgtools_NSCLC_Radiogenomics.csv"

@pytest.fixture
def lung4DSummaryFilePath():
    return "tests/.imgtools/imgtools_4D-Lung.csv"

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
        matchCTtoSegmentation(nsclcSummaryFilePath, segType = 'SEG',
                              outputFilePath = badFilePath)

