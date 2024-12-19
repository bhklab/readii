import numpy as np
import pandas as pd
import pytest

from pathlib import Path
from readii.io.loaders.features import loadFeatureFilesFromImageTypes


@pytest.fixture(scope="session")
def original_feature_file_path(tmp_path_factory):
    # Create a 10x10 matrix with random float values between 0 and 1
    random_matrix = np.random.default_rng(seed=10).random((10,10))
    # Convert to dataframe and name the columns feature1, feature2, etc.
    random_feature_df = pd.DataFrame(random_matrix, columns=[f"feature_{i+1}" for i in range(10)])
    # Save the dataframe to a temporary file
    feature_file_path = tmp_path_factory.mktemp("feature") / "features_original.csv"
    random_feature_df.to_csv(feature_file_path)
    return feature_file_path


def test_load_single_feature_file(original_feature_file_path):   
    feature_sets = loadFeatureFilesFromImageTypes(extracted_feature_dir=original_feature_file_path.parent, image_types=["original"], drop_labels=False)
    assert isinstance(feature_sets, dict), "Return should be a dictionary."
    assert len(feature_sets) == 1, "Should only have one feature file per image type."
    assert "original" in feature_sets, "Not finding the specified image type feature file (original) or keys are not correctly named."