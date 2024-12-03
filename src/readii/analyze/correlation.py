import pandas as pd
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.linalg import issymmetric


def getFeatureCorrelations(vertical_features:pd.DataFrame,
                           horizontal_features:pd.DataFrame,
                           method:Optional[str] = "pearson",
                           vertical_feature_name:Optional[str] = "",
                           horizontal_feature_name:Optional[str] = ""):
    """ Function to calculate correlation between two sets of features.

    Parameters
    ----------
    vertical_features : pd.DataFrame
        Dataframe containing features to calculate correlations with.
    horizontal_features : pd.DataFrame
        Dataframe containing features to calculate correlations with.
    method : str
        Method to use for calculating correlations. Default is "pearson".
    vertical_feature_name : str
        Name of the vertical features to use as suffix in correlation dataframe. Default is blank "".
    horizontal_feature_name : str
        Name of the horizontal features to use as suffix in correlation dataframe. Default is blank "".
    
    Returns
    -------
    correlation_matrix : pd.DataFrame
        Dataframe containing correlation values.
    """
    # Join the features into one dataframe
    # Use inner join to keep only the rows that have a value in both vertical and horizontal features
    features_to_correlate = vertical_features.join(horizontal_features, 
                                                how='inner', 
                                                lsuffix=f"_{vertical_feature_name}", 
                                                rsuffix=f"_{horizontal_feature_name}") 

    # Calculate correlation between vertical features and horizontal features
    correlation_matrix = features_to_correlate.corr(method=method)

    return correlation_matrix
