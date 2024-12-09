import pandas as pd
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.linalg import issymmetric


def getFeatureCorrelations(vertical_features:pd.DataFrame,
                           horizontal_features:pd.DataFrame,
                           method:str = "pearson",
                           vertical_feature_name:Optional[str] = "",
                           horizontal_feature_name:Optional[str] = ""):
    """ Function to calculate correlation between two sets of features.

    Parameters
    ----------
    vertical_features : pd.DataFrame
        Dataframe containing features to calculate correlations with. Index must be the same as the index of the horizontal_features dataframe.
    horizontal_features : pd.DataFrame
        Dataframe containing features to calculate correlations with. Index must be the same as the index of the vertical_features dataframe.
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
    # Check that features are dataframes
    assert isinstance(vertical_features, pd.DataFrame), "vertical_features must be a pandas DataFrame"
    assert isinstance(horizontal_features, pd.DataFrame), "horizontal_features must be a pandas DataFrame"

    if method not in ["pearson", "spearman", "kendall"]:
        raise ValueError("Correlation method must be one of 'pearson', 'spearman', or 'kendall'.")

    if not vertical_features.index.equals(horizontal_features.index):
        raise ValueError("Vertical and horizontal features must have the same index to calculate correlation. Set the index to the intersection of patient IDs.")

    # Add _ to beginnging of feature names if they are not blank so they can be used as suffixes
    if vertical_feature_name: vertical_feature_name = f"_{vertical_feature_name}"
    if horizontal_feature_name: horizontal_feature_name = f"_{horizontal_feature_name}"

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
        raise ValueError(f"Error calculating correlation matrix: {e}")

    return correlation_matrix


def plotCorrelationHeatmap(correlation_matrix_df:pd.DataFrame,
                           diagonal:Optional[bool] = False,
                           triangle:Optional[str] = "lower",
                           cmap:Optional[str] = "nipy_spectral",
                           xlabel:Optional[str] = "",
                           ylabel:Optional[str] = "",
                           title:Optional[str] = "",
                           subtitle:Optional[str] = "",
                           show_tick_labels:Optional[bool] = False
                           ):
    """Function to plot a correlation heatmap.

    Parameters
    ----------
    correlation_matrix_df : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    diagonal : bool, optional
        Whether to only plot half of the matrix. The default is False.
    triangle : str, optional
        Which triangle half of the matrixto plot. The default is "lower".
    xlabel : str, optional
        Label for the x-axis. The default is "".
    ylabel : str, optional
        Label for the y-axis. The default is "".
    title : str, optional
        Title for the plot. The default is "".
    subtitle : str, optional
        Subtitle for the plot. The default is "".
    show_tick_labels : bool, optional
        Whether to show the tick labels on the x and y axes. These would be the feature names. The default is False.

    Returns
    -------
    corr_fig : matplotlib.pyplot.figure
        Figure object containing a Seaborn heatmap.
    """

    if diagonal:
        # Set up mask for hiding half the matrix in the plot
        if triangle == "lower":
            # Mask out the upper right triangle half of the matrix
            mask = np.triu(correlation_matrix_df)
        elif triangle == "upper":
            # Mask out the lower left triangle half of the matrix
            mask = np.tril(correlation_matrix_df)
        else:
            raise ValueError("If diagonal is True, triangle must be either 'lower' or 'upper'.")
    else:
        # The entire correlation matrix will be visisble in the plot
        mask = None
    
    # Set a default title if one is not provided
    if not title:
        title = "Correlation Heatmap"

    # Set up figure and axes for the plot
    corr_fig, corr_ax = plt.subplots()

    # Plot the correlation matrix
    corr_ax = sns.heatmap(correlation_matrix_df,
                         mask = mask,
                         cmap=cmap,
                         vmin=-1.0,
                         vmax=1.0)
    
    if not show_tick_labels:
        # Remove the individual feature names from the axes
        corr_ax.set_xticklabels(labels=[])
        corr_ax.set_yticklabels(labels=[])

    # Set axis labels
    corr_ax.set_xlabel(xlabel)
    corr_ax.set_ylabel(ylabel)
    
    # Set title and subtitle
    # Suptitle is the super title, which will be above the title
    plt.title(subtitle, fontsize=12)
    plt.suptitle(title, fontsize=14)
    
    return corr_fig



def getVerticalSelfCorrelations(correlation_matrix:pd.DataFrame,
                                num_vertical_features:int):
    """ Function to get the vertical (y-axis) self correlations from a correlation matrix. Gets the top left quadrant of the correlation matrix.

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
    if num_vertical_features > correlation_matrix.shape[0]:
        raise ValueError(f"Number of vertical features ({num_vertical_features}) is greater than the number of rows in the correlation matrix ({correlation_matrix.shape[0]}).")
    
    if num_vertical_features > correlation_matrix.shape[1]:
        raise ValueError(f"Number of vertical features ({num_vertical_features}) is greater than the number of columns in the correlation matrix ({correlation_matrix.shape[1]}).")

    # Get the correlation matrix for vertical vs vertical - this is the top left corner of the matrix
    return correlation_matrix.iloc[0:num_vertical_features, 0:num_vertical_features]



def getHorizontalSelfCorrelations(correlation_matrix:pd.DataFrame,
                                  num_horizontal_features:int):
    """ Function to get the horizontal (x-axis) self correlations from a correlation matrix. Gets the bottom right quadrant of the correlation matrix.

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
    
    if num_horizontal_features > correlation_matrix.shape[0]:
        raise ValueError(f"Number of horizontal features ({num_horizontal_features}) is greater than the number of rows in the correlation matrix ({correlation_matrix.shape[0]}).")
    
    if num_horizontal_features > correlation_matrix.shape[1]:
        raise ValueError(f"Number of horizontal features ({num_horizontal_features}) is greater than the number of columns in the correlation matrix ({correlation_matrix.shape[1]}).")

    # Get the index of the start of the horizontal correlations
    start_of_horizontal_correlations = len(correlation_matrix.columns) - num_horizontal_features

    # Get the correlation matrix for horizontal vs horizontal - this is the bottom right corner of the matrix
    return correlation_matrix.iloc[start_of_horizontal_correlations:, start_of_horizontal_correlations:]



def getCrossCorrelationMatrix(correlation_matrix:pd.DataFrame,
                              num_vertical_features:int):
    """ Function to get the cross correlation matrix subsection for a correlation matrix. Gets the top right quadrant of the correlation matrix so vertical and horizontal features are correctly labeled.

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

    if num_vertical_features > correlation_matrix.shape[0]:
        raise ValueError(f"Number of vertical features ({num_vertical_features}) is greater than the number of rows in the correlation matrix ({correlation_matrix.shape[0]}).")
    
    if num_vertical_features > correlation_matrix.shape[1]:
        raise ValueError(f"Number of vertical features ({num_vertical_features}) is greater than the number of columns in the correlation matrix ({correlation_matrix.shape[1]}).")
    
    return correlation_matrix.iloc[0:num_vertical_features, num_vertical_features:]