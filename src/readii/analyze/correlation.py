import pandas as pd

from readii.data.select import validateDataframeSubsetSelection
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



def getVerticalSelfCorrelations(correlation_matrix:pd.DataFrame,
                                num_vertical_features:int) -> pd.DataFrame:
    """Get the vertical (y-axis) self correlations from a correlation matrix. Gets the top left quadrant of the correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to get the vertical self correlations from.
    num_vertical_features : int
        Number of vertical features in the correlation matrix.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the vertical self correlations from the correlation matrix.    
    """
    try: 
        validateDataframeSubsetSelection(correlation_matrix, num_vertical_features, num_vertical_features)
    except ValueError as e:
        msg = "Number of vertical features provided is greater than the number of rows or columns in the correlation matrix."
        logger.exception(msg)
        raise e

    # Get the correlation matrix for vertical vs vertical - this is the top left corner of the matrix
    return correlation_matrix.iloc[0:num_vertical_features, 0:num_vertical_features]



def getHorizontalSelfCorrelations(correlation_matrix:pd.DataFrame,
                                  num_horizontal_features:int) -> pd.DataFrame:
    """Get the horizontal (x-axis) self correlations from a correlation matrix. Gets the bottom right quadrant of the correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to get the horizontal self correlations from.
    num_horizontal_features : int
        Number of horizontal features in the correlation matrix.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the horizontal self correlations from the correlation matrix.
    """
    try: 
        validateDataframeSubsetSelection(correlation_matrix, num_horizontal_features, num_horizontal_features)
    except ValueError as e: 
        msg = "Number of horizontalfeatures provided is greater than the number of rows or columns in the correlation matrix."
        logger.exception(msg)
        raise e

    # Get the index of the start of the horizontal correlations
    start_of_horizontal_correlations = len(correlation_matrix.columns) - num_horizontal_features

    # Get the correlation matrix for horizontal vs horizontal - this is the bottom right corner of the matrix
    return correlation_matrix.iloc[start_of_horizontal_correlations:, start_of_horizontal_correlations:]



def getCrossCorrelationMatrix(correlation_matrix:pd.DataFrame,
                              num_vertical_features:int) -> pd.DataFrame:
    """Get the cross correlation matrix subsection for a correlation matrix. Gets the top right quadrant of the correlation matrix so vertical and horizontal features are correctly labeled.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to get the cross correlation matrix subsection from.
    num_vertical_features : int
        Number of vertical features in the correlation matrix.
    
    Returns
    -------
    pd.DataFrame
        Dataframe containing the cross correlations from the correlation matrix.
    """
    try:
        validateDataframeSubsetSelection(correlation_matrix, num_vertical_features, num_vertical_features)
    except ValueError as e:
        msg = "Number of vertical features provided is greater than the number of rows or columns in the correlation matrix."
        logger.exception(msg)
        raise e
    
    return correlation_matrix.iloc[0:num_vertical_features, num_vertical_features:]