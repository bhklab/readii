import pandas as pd

from readii.utils import logger


def getFeatureCorrelations(vertical_features:pd.DataFrame,
                           horizontal_features:pd.DataFrame,
                           method:str = "pearson",
                           vertical_feature_name:str = '_vertical',
                           horizontal_feature_name:str = '_horizontal') -> pd.DataFrame:
    """Calculate correlation between two sets of features.

    Parameters
    ----------
    vertical_features : pd.DataFrame
        Dataframe containing features to calculate correlations with. Index must be the same as the index of the horizontal_features dataframe.
    horizontal_features : pd.DataFrame
        Dataframe containing features to calculate correlations with. Index must be the same as the index of the vertical_features dataframe.
    method : str
        Method to use for calculating correlations. Default is "pearson".
    vertical_feature_name : str
        Name of the vertical features to use as suffix in correlation dataframe. Default is "_vertical".
    horizontal_feature_name : str
        Name of the horizontal features to use as suffix in correlation dataframe. Default is "_horizontal".
    
    Returns
    -------
    correlation_matrix : pd.DataFrame
        Dataframe containing correlation values.
    """
    # Check that features are dataframes
    if not isinstance(vertical_features, pd.DataFrame):
        msg = "vertical_features must be a pandas DataFrame"
        logger.exception(msg)
        raise TypeError()
    if not isinstance(horizontal_features, pd.DataFrame):
        msg = "horizontal_features must be a pandas DataFrame"
        logger.exception(msg)
        raise TypeError()
    
    # Check for empty DataFrames  
    if vertical_features.empty or horizontal_features.empty:  
        msg = "Cannot calculate correlations with empty DataFrames"  
        logger.exception(msg)  
        raise ValueError(msg)

    if method not in ["pearson", "spearman", "kendall"]:
        msg = "Correlation method must be one of 'pearson', 'spearman', or 'kendall'."
        logger.exception(msg)
        raise ValueError()

    if not vertical_features.index.equals(horizontal_features.index):
        msg = "Vertical and horizontal features must have the same index to calculate correlation. Set the index to the intersection of patient IDs."
        logger.exception(msg)
        raise ValueError()

    # Add _ to beginnging of feature names if they don't start with _ so they can be used as suffixes
    if not vertical_feature_name.startswith("_"): 
        vertical_feature_name = f"_{vertical_feature_name}"
    if not horizontal_feature_name.startswith("_"): 
        horizontal_feature_name = f"_{horizontal_feature_name}"

    # Join the features into one dataframe
    # Use inner join to keep only the rows that have a value in both vertical and horizontal features
    features_to_correlate = vertical_features.join(horizontal_features, 
                                                   how='inner', 
                                                   lsuffix=vertical_feature_name, 
                                                   rsuffix=horizontal_feature_name) 

    try:
        # Calculate correlation between vertical features and horizontal features
        correlation_matrix = features_to_correlate.corr(method=method)
    except Exception as e:
        msg = f"Error calculating correlation matrix: {e}"
        logger.exception(msg)
        raise e

    return correlation_matrix



def getSelfCorrelations(correlation_matrix:pd.DataFrame,
                        feature_type_name:str) -> pd.DataFrame:
    """Get self correlations from a correlation matrix based on feature type name suffix in index.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to get the vertical self correlations from.
    feature_type_name : str
        Name of the feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the vertical self correlations from the correlation matrix.    
    """
    # Get the rows and columns with the same feature type name suffix
    self_correlations = correlation_matrix.filter(like=feature_type_name, axis=0).filter(like=feature_type_name, axis=1)
        
    if self_correlations.empty:
        msg = f"No features with found with {feature_type_name} suffix in the correlation matrix."
        logger.exception(msg)
        raise ValueError()

    return self_correlations



def getCrossCorrelations(correlation_matrix:pd.DataFrame,
                         vertical_feature_name:str = "_vertical",
                         horizontal_feature_name:str = "_horizontal") -> pd.DataFrame:
    """Get the cross correlation matrix subsection for a correlation matrix. Gets the top right quadrant of the correlation matrix so vertical and horizontal features are correctly labeled.

    Parameters
    ----------    
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to get the cross correlation matrix subsection from.
    vertical_feature_name : str
        Name of the vertical feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix index.
    horizontal_feature_name : str
        Name of the horizontal feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix columns.

    Returns
    -------
    cross_correlations : pd.DataFrame
        Dataframe containing the cross correlations from the correlation matrix.
    """
    # Get the rows with the vertical feature name suffix and the columns with the horizontal feature name suffix
    cross_correlations = correlation_matrix.filter(like=vertical_feature_name, axis=0).filter(like=horizontal_feature_name, axis=1)
    
    if cross_correlations.empty:
        msg = f"No features with found with {vertical_feature_name} and {horizontal_feature_name} suffix in the correlation matrix."
        logger.exception(msg)
        raise ValueError()
    
    return cross_correlations



def getSelfAndCrossCorrelations(correlation_matrix:pd.DataFrame,
                                vertical_feature_name:str = '_vertical',
                                horizontal_feature_name:str = '_horizontal') -> pd.DataFrame:
    """Get the vertical and horizontal self correlations and cross correlations from a correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to get the self and cross correlations from.
    vertical_feature_name : str
        Name of the vertical feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix.
    horizontal_feature_name : str
        Name of the horizontal feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix.

    Returns
    -------
    vertical_correlations : pd.DataFrame
        Dataframe containing the vertical self correlations from the correlation matrix.
    horizontal_correlations : pd.DataFrame
        Dataframe containing the horizontal self correlations from the correlation matrix.
    cross_correlations : pd.DataFrame
        Dataframe containing the cross correlations from the correlation matrix.
    """
    try:
        vertical_correlations, horizontal_correlations = getSelfCorrelations(correlation_matrix, vertical_feature_name), getSelfCorrelations(correlation_matrix, horizontal_feature_name)

    except Exception as e:
        msg = f"Error getting self correlations from correlation matrix: {e}"
        logger.exception(msg)
        raise e
    
    try:
        cross_correlations = getCrossCorrelations(correlation_matrix, vertical_feature_name, horizontal_feature_name)
    except Exception as e:
        msg = f"Error getting cross correlations from correlation matrix: {e}"
        logger.exception(msg)
        raise e

    return vertical_correlations, horizontal_correlations, cross_correlations