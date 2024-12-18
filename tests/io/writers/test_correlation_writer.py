import pytest

import pandas as pd
import numpy as np
from pathlib import Path
from readii.analyze.correlation import getFeatureCorrelations
from readii.io.writers.correlation_writer import CorrelationWriter, CorrelationWriterValidationError, CorrelationWriterError, CorrelationWriterIOError # type: ignore

@pytest.fixture
def random_feature_correlations():
    # Create a 10x10 matrix with random float values between 0 and 1
    random_matrix = np.random.default_rng(seed=10).random((10,10))
    # Convert to dataframe and name the columns feature1, feature2, etc.
    random_df = pd.DataFrame(random_matrix, columns=[f"feature_{i+1}" for i in range(10)])
    # Calculate correlation
    return getFeatureCorrelations(random_df, random_df)
    

@pytest.fixture
def corr_writer(tmp_path):
    """Fixture for creating a CorrelationWriter instance."""
    return CorrelationWriter(
        root_directory=tmp_path,
        filename_format="{CorrelationType}_correlation_matrix.csv",
        overwrite=False,
        create_dirs=True,
    )

@pytest.mark.parametrize("correlation_df", ["not_a_correlation_df", 12345, pd.DataFrame()])
def test_save_invalid_correlation(corr_writer, correlation_df):
    """Test saving an invalid image."""
    with pytest.raises(CorrelationWriterValidationError):
        corr_writer.save(correlation_df, CorrelationType="Pearson")

@pytest.mark.parametrize("correlation_df", ["random_feature_correlations"])
def test_save_valid_correlation(corr_writer, request, correlation_df):
    """Test saving a valid correlation dataframe."""
    correlation_df = request.getfixturevalue(correlation_df)
    out_path = corr_writer.save(correlation_df, CorrelationType="Pearson")
    assert out_path.exists()

def test_save_existing_file_without_overwrite(corr_writer, random_feature_correlations):
    """Test saving when file already exists and overwrite is False."""
    corr_writer.save(random_feature_correlations, CorrelationType="Pearson")
    with pytest.raises(CorrelationWriterIOError):
        corr_writer.save(random_feature_correlations, CorrelationType="Pearson")

def test_save_existing_file_with_overwrite(corr_writer, random_feature_correlations):
    """Test saving when file already exists and overwrite is True."""
    corr_writer.overwrite = True
    corr_writer.save(random_feature_correlations, CorrelationType="Pearson")
    assert corr_writer.save(random_feature_correlations, CorrelationType="Pearson").exists()

@pytest.mark.parametrize("filename_format", ["{CorrelationType}_correlation_matrix.csv", "{CorrelationType}_correlation_matrix.xlsx"])
def test_save_with_different_filename_formats(corr_writer, random_feature_correlations, filename_format):
    """Test saving with different filename formats."""
    corr_writer.filename_format = filename_format
    out_path = corr_writer.save(random_feature_correlations, CorrelationType="Pearson")
    assert out_path.exists()
