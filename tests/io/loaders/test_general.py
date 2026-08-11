from readii.io.loaders.general import loadImageDatasetConfig
import pytest

@pytest.fixture
def nsclcConfigDirPath():
    return "tests/NSCLC_Radiogenomics"

@pytest.fixture
def lung4DConfigDirPath():
    return "tests/4D-Lung"

@pytest.fixture
def expected_image_types():
    return ["original", "shuffled_full","shuffled_roi","shuffled_non_roi","randomized_sampled_full","randomized_sampled_roi","randomized_sampled_non_roi"]


def test_NSCLC_loadImageDatasetConfig(nsclcConfigDirPath, expected_image_types):
    config = loadImageDatasetConfig("NSCLC_Radiogenomics", nsclcConfigDirPath)
    assert config["dataset_name"] == "NSCLC_Radiogenomics"
    assert config["image_types"] == expected_image_types
    assert config["outcome_variables"]["event_label"] == "Survival Status"
    assert config["outcome_variables"]["event_value_mapping"] == {'Alive': 0, 'Dead': 1}

def test_lung4D_loadImageDatasetConfig(lung4DConfigDirPath, expected_image_types):
    config = loadImageDatasetConfig("4D-Lung", lung4DConfigDirPath)
    assert config["dataset_name"] == "4D-Lung"
    assert config["image_types"] == expected_image_types
    assert config["outcome_variables"]["event_label"] is None
    assert config["outcome_variables"]["event_value_mapping"] is None