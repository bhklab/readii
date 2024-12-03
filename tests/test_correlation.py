from readii.analyze.correlation import (
    getFeatureCorrelations,
    plotCorrelationHeatmap,
)

import pytest
import collections
import pandas as pd
import os 

@pytest.fixture
def nsclc_radiomic_features():
    return pd.read_csv("tests/output/features/radiomicfeatures_original_NSCLC_Radiogenomics.csv")

@pytest.fixture
def lung4D_radiomic_features():
    return pd.read_csv("tests/output/features/radiomicfeatures_original_4D-Lung.csv")


@pytest.mark.parametrize(
        "features",
        [
            ("nsclc_radiomic_features"),
            ("lung4D_radiomic_features")
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
    actual = getFeatureCorrelations(vertical_features = features,
                                    horizontal_features = features,
                                    method = correlation_method
                                    )
    assert isinstance(actual, pd.DataFrame), \
        "Wrong return type, expect a pandas DataFrame"
    assert actual.shape[0] == 2*features.shape[1], \
        "Wrong return size, should be the same as the number of features"