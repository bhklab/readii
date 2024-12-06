from readii.analyze.correlation import (
    getFeatureCorrelations,
    plotCorrelationHeatmap,
)

from readii.data.process import dropUpToFeature

import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def random_feature_matrix():
    # Create a 10x10 matrix with random float values between 0 and 1
    random_matrix = np.random.default_rng(seed=10).random((10,10))
    # Convert to dataframe and name the columns feature1, feature2, etc.
    return pd.DataFrame(random_matrix, columns=[f"feature_{i+1}" for i in range(10)])

@pytest.mark.parametrize(
        "features",
        [
            ("random_feature_matrix")
        ],
        "correlation_method",
        [
            ("pearson"),
            ("spearman"),
            ("random")
        ]
)
def test_getFeatureCorrelations(features, correlation_method, request):
    """Test getting correlation matrix for a set of features"""
    features = request.getfixturevalue(features)
    correlation_method = request.getfixturevalue(correlation_method)

    features_to_corr = features.join(features, how='inner')
    expected = features_to_corr.corr(method=correlation_method)

    actual = getFeatureCorrelations(vertical_features = features,
                                    horizontal_features = features,
                                    method = correlation_method
                                    )
    assert isinstance(actual, pd.DataFrame), \
        "Wrong return type, expect a pandas DataFrame"
    assert actual.shape[0] == 2*features.shape[1], \
        "Wrong return size, should be the same as the number of features"
    assert actual.equals(expected), \
        "Correlation values is incorrect for the given features"