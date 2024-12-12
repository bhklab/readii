from readii.io.loaders.general import *
import pytest

@pytest.fixture
def nsclcConfigDirPath():
    return "tests/NSCLC_Radiogenomics"

@pytest.fixture
def lung4DConfigDirPath():
    return "tests/4D-Lung"

def test_NSCLC_loadImageDatasetConfig(nsclcConfigDirPath):
    config = loadImageDatasetConfig("NSCLC_Radiogenomics", nsclcConfigDirPath)
    assert config["dataset_name"] == "NSCLC_Radiogenomics"
    assert config["image_types"] == ["original", "shuffled_full","shuffled_roi","shuffled_non_roi","randomized_sampled_full","randomized_sampled_roi","randomized_sampled_non_roi"]
    assert config["outcome_variables"]["event_label"] == "Survival Status"
    assert config["outcome_variables"]["event_value_mapping"] == {'Alive': 0, 'Dead': 1}

def test_lung4D_loadImageDatasetConfig(lung4DConfigDirPath):
    config = loadImageDatasetConfig("4D-Lung", lung4DConfigDirPath)
    assert config["dataset_name"] == "4D-Lung"
    assert config["image_types"] == ["original", "shuffled_full","shuffled_roi","shuffled_non_roi","randomized_sampled_full","randomized_sampled_roi","randomized_sampled_non_roi"]
    assert config["outcome_variables"]["event_label"] == None
    assert config["outcome_variables"]["event_value_mapping"] == None