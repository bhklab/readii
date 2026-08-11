from readii.analyze.correlation import (
    getFeatureCorrelations
)

import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def random_features():
    # Create a 10x10 matrix with random float values between 0 and 1
    random_matrix = np.random.default_rng(seed=10).random((10,10))
    # Convert to dataframe and name the columns feature1, feature2, etc.
    return pd.DataFrame(random_matrix, columns=[f"feature_{i+1}" for i in range(10)])

@pytest.mark.parametrize(
    "correlation_method",
    [
        "pearson",
        "spearman",
        "kendall"
    ]
)
def test_methods_getFeatureCorrelation(correlation_method, random_features):
    """Test getting correlation matrix for a set of random_features with pearson and spearman correlation methods"""

    features_to_corr = random_features.join(random_features, how='inner', lsuffix='_vertical', rsuffix='_horizontal')
    expected = features_to_corr.corr(method=correlation_method)

    actual = getFeatureCorrelations(vertical_features = random_features,
                                    horizontal_features = random_features,
                                    method = correlation_method
                                    )
    assert isinstance(actual, pd.DataFrame), \
        "Wrong return type, expect a pandas DataFrame"
    assert actual.shape[0] == 2*random_features.shape[1], \
        "Wrong return size, should be double the number of input features"
    assert actual.equals(expected), \
        f"{correlation_method} correlation values are incorrect for the input features"


def test_defaults_getFeatureCorrelations(random_features):
    """Test the default argument behaviours of getFeatureCorrelations. Should be a Pearson correlation matrix with _vertical and _horizontal suffixes on the feature names"""
    features_to_corr = random_features.join(random_features, how='inner', lsuffix='_vertical', rsuffix='_horizontal')
    expected = features_to_corr.corr(method="pearson")

    actual = getFeatureCorrelations(vertical_features = random_features,
                                    horizontal_features = random_features)
    assert isinstance(actual, pd.DataFrame), \
        "Wrong return type, expect a pandas DataFrame"
    assert actual.shape[0] == 2*random_features.shape[1], \
        "Wrong return size, should be double the number of the input features"
    assert actual.equals(expected), \
        "Pearson correlation values are incorrect for the input features"
    assert actual.columns.equals(expected.columns), \
        "Column names are incorrect. Should be the input features with _vertical and _horizontal suffixes"


@pytest.mark.parametrize(
    "correlation_method",
    [
        "random",
        ""
    ]
)
def test_wrongMethod_getFeatureCorrelations(random_features, correlation_method):
    """Check ValueError is raised when incorrect correlation method is passed"""
    with pytest.raises(ValueError):
        getFeatureCorrelations(vertical_features = random_features,
                                horizontal_features = random_features,
                                method = correlation_method
                                )

@pytest.mark.parametrize(
    "wrong_features",
    [
        np.random.default_rng(seed=10).random((10,10)),
        "Just a string",
        {"feat1": 34, "feat2": 10000, "feat3": 3.141592}
    ]
)
def test_wrongFeatures_getFeatureCorrelations(random_features, wrong_features):
    """Check ValueError is raised when incorrect features are passed"""
    with pytest.raises(TypeError):
        getFeatureCorrelations(vertical_features = random_features,
                                horizontal_features = wrong_features,
                                method = "pearson"
                                )
    with pytest.raises(TypeError):
        getFeatureCorrelations(vertical_features = wrong_features,
                                horizontal_features = random_features,
                                method = "pearson"
                                )

@pytest.mark.parametrize(
    "vertical_feature_name, horizontal_feature_name, expected_vertical, expected_horizontal",
    [
        ("type_A", "type_B", [f"feature_{i+1}_type_A" for i in range(10)], [f"feature_{i+1}_type_B" for i in range(10)]),
        ("_type_C", "_type_D", [f"feature_{i+1}_type_C" for i in range(10)], [f"feature_{i+1}_type_D" for i in range(10)]),
    ]
)
def test_featureNames_getFeatureCorrelations(random_features, vertical_feature_name, horizontal_feature_name, expected_vertical, expected_horizontal):
    """ Check that feature names with and without _ prefix are handled correctly"""

    actual = getFeatureCorrelations(vertical_features=random_features,
                                    horizontal_features=random_features,
                                    vertical_feature_name=vertical_feature_name,
                                    horizontal_feature_name=horizontal_feature_name)
    
    assert list(actual.columns) == expected_vertical + expected_horizontal, \
        "Column names are incorrect, check underscore prefix handling when adding the vertical and horizontal feature names. Should be [feature]_vertical_feature_name and [feature]_horizontal_feature_name."
    assert list(actual.index) == expected_vertical + expected_horizontal, \
        "Index values are incorrect, check underscore prefix handling when adding the vertical and horizontal feature names. Should be [feature]_vertical_feature_name and [feature]_horizontal_feature_name."
    