import pytest

from pathlib import Path
from readii.io.loaders.features import loadFeatureFilesFromImageTypes


@pytest.fixture
def extracted_feature_4D_lung():
    return Path("tests/4D-lung/results/features/")

def test_loadFeatureFilesFromImageTypes(extracted_feature_4D_lung):
    feature_sets = loadFeatureFilesFromImageTypes(extracted_feature_4D_lung, image_types=["original"], drop_labels=False)
    assert isinstance(feature_sets, dict), "Return should be a dictionary."
    assert len(feature_sets) == 1, "Should only have one feature file per image type."
    assert "original" in feature_sets, "Not finding the specified image type feature file (original) or keys are not correctly named."