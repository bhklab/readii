from readii.analyze.correlation import getFeatureCorrelations
from readii.io.writers.plot_writer import PlotWriter

from readii.analyze.plot_correlation import (
    saveCorrelationHeatmap,
    plotCorrelationHeatmap,
    saveCorrelationHistogram,
    plotCorrelationHistogram,
    plotSelfCorrHeatmap,
    plotCrossCorrHeatmap,
    plotSelfCorrHistogram,
    plotCrossCorrHistogram
)

from matplotlib.figure import Figure
from pathlib import Path
import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def correlations_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("correlations")

@pytest.fixture(scope="module")
def vertical_feature_name():
    return "vertical"

@pytest.fixture(scope="module")
def horizontal_feature_name():
    return "horizontal"

@pytest.fixture(scope="module")
def correlation_method():
    return "pearson"

@pytest.fixture(scope="module")
def correlation_matrix(correlation_method, vertical_feature_name, horizontal_feature_name):
    # Create two 10x10 matrices with random float values between 0 and 1
    random_matrix_vertical = np.random.default_rng(seed=10).random((10,10))
    random_matrix_horizontal = np.random.default_rng(seed=10).random((10,10))

    # Generate dummy feature names
    feature_list = [f"feature_{i+1}" for i in range(10)]

    # Convert to dataframe and name the columns and index with the feature list
    vertical_df = pd.DataFrame(random_matrix_vertical, columns=feature_list, index=feature_list)
    horizontal_df = pd.DataFrame(random_matrix_horizontal, columns=feature_list, index=feature_list)

    return getFeatureCorrelations(vertical_df, horizontal_df, correlation_method, vertical_feature_name, horizontal_feature_name)


def test_make_heatmap_defaults(correlation_matrix):
    """Test making a heatmap from a correlation matrix with default arguments"""
    corr_fig = plotCorrelationHeatmap(correlation_matrix)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert corr_fig.get_suptitle() == "Correlation Heatmap", \
        "Wrong title, expect Correlation Heatmap"


def test_make_histogram_defaults(correlation_matrix):
    """Test making a histogram from a correlation matrix with default arguments"""
    corr_fig, bin_values, bin_edges = plotCorrelationHistogram(correlation_matrix)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert bin_values[0] == 4.0, \
        f"Wrong first bin value, expect 4.0, got {bin_values[0]}"
    assert bin_values[-1] == 30.0, \
        f"Wrong last value, expect 30.0, got {bin_values[-1]}"



@pytest.mark.parametrize(
    "triangle",
    [
        "lower",
        "upper"
    ]
)
def test_diagonal_heatmap(correlation_matrix, triangle):
    """Test making a heatmap from a correlation matrix with diagonal set to True"""
    corr_fig = plotCorrelationHeatmap(correlation_matrix, diagonal=True, triangle=triangle)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert corr_fig.get_suptitle() == f"Correlation Heatmap", \
        "Wrong title, expect Correlation Heatmap"
    

@pytest.mark.parametrize(
    "correlation_type, feature_types",
    [
        ("pearson_self", ["vertical"]),
        ("pearson_cross", ["vertical", "horizontal"]),
    ]
)
def test_save_corr_heatmap(correlation_matrix, correlations_dir, correlation_type, feature_types):
    """Test saving a heatmap from a cross-correlation matrix"""
    corr_fig = plotCorrelationHeatmap(correlation_matrix)

    expected_path = correlations_dir / "heatmap" / "nipy_spectral" / ("_vs_".join(feature_types)) + f"_{correlation_type}_correlation_heatmap.png"

    actual_path = saveCorrelationHeatmap(corr_fig,
                                         correlations_dir,
                                         cmap="nipy_spectral",
                                         feature_types=feature_types,
                                         correlation_type=correlation_type)
    assert actual_path == expected_path, \
        "Wrong path returned, expect {expected_path}"
    assert actual_path.exists(), \
        "Figure is not being saved to path provided or at all."



@pytest.mark.parametrize(
    "correlation_type, feature_types",
    [
        ("pearson_self", ["vertical"]),
        ("pearson_cross", ["vertical", "horizontal"]),
    ]
)
def test_save_corr_histogram(correlation_matrix, correlations_dir, correlation_type, feature_types):
    """Test saving a histogram from a correlation matrix"""
    corr_fig, _, _ = plotCorrelationHistogram(correlation_matrix)
    
    expected_path = correlations_dir / "histogram" / ("_vs_".join(feature_types)) + f"_{correlation_type}_correlation_histogram.png"

    actual_path = saveCorrelationHistogram(corr_fig,
                                           correlations_dir,
                                           feature_types=feature_types,
                                           correlation_type=correlation_type)
    assert actual_path == expected_path, \
        "Wrong path returned, expect {expected_path}"  
    assert actual_path.exists(), \
        "Figure is not being saved to path provided or at all."
    


def test_plot_selfcorr_heatmap_defaults(correlation_matrix, vertical_feature_name):
    """Test plotting a self-correlation heatmap from a correlation matrix"""
    corr_fig = plotSelfCorrHeatmap(correlation_matrix,
                                   feature_type_name=vertical_feature_name)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert corr_fig.get_suptitle() == f"Pearson Self Correlations", \
        "Wrong title, expect Pearson Self Correlations"
    assert corr_fig.get_axes()[0].get_title(), \
        "Wrong subtitle, expect vertical"
    

def test_plot_crosscorr_heatmap_defaults(correlation_matrix, vertical_feature_name, horizontal_feature_name):
    """Test plotting a cross-correlation heatmap from a correlation matrix"""
    corr_fig = plotCrossCorrHeatmap(correlation_matrix,
                                    vertical_feature_name=vertical_feature_name,
                                    horizontal_feature_name=horizontal_feature_name)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert corr_fig.get_suptitle() == f"Pearson Cross Correlations", \
        "Wrong title, expect Pearson Cross Correlations"
    assert corr_fig.get_axes()[0].get_title(), \
        "Wrong subtitle, expect vertical vs horizontal"


def test_plot_selfcorr_histogram_defaults(correlation_matrix, vertical_feature_name):
    """Test plotting a self-correlation histogram from a correlation matrix"""
    corr_fig = plotSelfCorrHistogram(correlation_matrix,
                                     feature_type_name=vertical_feature_name)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert corr_fig.get_suptitle() == f"Distribution of Pearson Self Correlations", \
        "Wrong title, expect Distribution of Pearson Self Correlations"
    assert corr_fig.get_axes()[0].get_title(), \
        "Wrong subtitle, expect vertical"


def test_plot_crosscorr_histogram_defaults(correlation_matrix, vertical_feature_name, horizontal_feature_name):
    """Test plotting a cross-correlation histogram from a correlation matrix"""
    corr_fig = plotCrossCorrHistogram(correlation_matrix,
                                      vertical_feature_name=vertical_feature_name,
                                      horizontal_feature_name=horizontal_feature_name)
    assert isinstance(corr_fig, Figure), \
        "Wrong return type, expect a matplotlib Figure"
    assert corr_fig.get_suptitle() == f"Distribution of Pearson Cross Correlations", \
        "Wrong title, expect Pearon Cross Correlations"
    assert corr_fig.get_axes()[0].get_title(), \
        "Wrong subtitle, expect vertical vs horizontal"