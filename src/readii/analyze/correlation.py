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
