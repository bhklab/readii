from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from scipy.linalg import issymmetric

from readii.utils import logger


def plotCorrelationHeatmap(correlation_matrix_df:pd.DataFrame,
                           diagonal:bool = False,
                           triangle:Optional[str] = "lower",
                           cmap:str = "nipy_spectral",
                           xlabel:str = "",
                           ylabel:Optional[str] = "",
                           title:Optional[str] = "",
                           subtitle:Optional[str] = "",
                           show_tick_labels:bool = False
                           ) -> Figure:
    """Plot a correlation dataframe as a heatmap.

    Parameters
    ----------
    correlation_matrix_df : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    diagonal : bool, optional
        Whether to only plot half of the matrix. The default is False.
    triangle : str, optional
        Which triangle half of the matrix to plot. Either "lower" or "upper". 
        The default is "lower".
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
        logger.debug(f"Creating {triangle} traingle mask for diagonal correlation plot.")
        # Set up mask for hiding half the matrix in the plot
        if triangle == "lower":
            # Mask out the upper right triangle half of the matrix
            mask = np.triu(correlation_matrix_df)
        elif triangle == "upper":
            # Mask out the lower left triangle half of the matrix
            mask = np.tril(correlation_matrix_df)
        else:
            msg = f"If diagonal is True, triangle must be either 'lower' or 'upper'. Got {triangle}."
            logger.exception(msg)
            raise ValueError()
    else:
        logger.debug("Creating full square correlation matrix plot.")
        # The entire correlation matrix will be visisble in the plot
        mask = None
    
    # Set a default title if one is not provided
    if not title:
        title = "Correlation Heatmap"

    # Set up figure and axes for the plot
    corr_fig, corr_ax = plt.subplots()

    # Plot the correlation matrix
    try:
        corr_ax = sns.heatmap(correlation_matrix_df,
                             mask = mask,
                             cmap=cmap,
                             vmin=-1.0,
                             vmax=1.0)
    except Exception as e:
        msg = f"Error generating heatmap: {e}"
        logger.exception(msg)
        raise e
    
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



def plotCorrelationHistogram(correlation_matrix:pd.DataFrame,
                             num_bins:int = 100,
                             xlabel:Optional[str] = "Correlations",
                             ylabel:Optional[str] = "Frequency",
                             y_lower_bound:int = 0,
                             y_upper_bound:Optional[int] = None,
                             title:Optional[str] = "Distribution of Correlations for Features",
                             subtitle:Optional[str] = "",
                             ) -> Figure:
    """Plot a histogram to show thedistribution of correlation values for a correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    num_bins : int, optional
        Number of bins to use for the distribution plot. The default is 100.
    xlabel : str, optional
        Label for the x-axis. The default is "Correlations".
    ylabel : str, optional
        Label for the y-axis. The default is "Frequency".
    y_lower_bound : int, optional
        Lower bound for the y-axis of the distribution plot. The default is 0.
    y_upper_bound : int, optional
        Upper bound for the y-axis of the distribution plot. The default is None.
    title : str, optional
        Title for the plot. The default is "Distribution of Correlations for Features".
    subtitle : str, optional
        Subtitle for the plot. The default is "".

    Returns
    -------
    dist_fig : plt.Figure
        Figure object containing the histogram of correlation values.
    bin_values : np.ndarray or list of arrays
        Numpy array containing the values in each bin for the histogram.
    bin_edges : np.ndarray
        Numpy array containing the bin edges for the histogram.
    """
    # Convert to numpy to use histogram function
    feature_correlation_arr = correlation_matrix.to_numpy()

    # Check if matrix is symmetric
    if issymmetric(feature_correlation_arr):
        logger.debug("Correlation matrix is symmetric.")
        # Get only the bottom left triangle of the correlation matrix since the matrix is symmetric 
        lower_half_idx = np.mask_indices(feature_correlation_arr.shape[0], np.tril)
        # This is a 1D array for binning and plotting
        correlation_vals = feature_correlation_arr[lower_half_idx]
    else:
        # Flatten the matrix to a 1D array for binning and plotting
        correlation_vals = feature_correlation_arr.flatten()

    # Set up figure and axes for the plot
    dist_fig, dist_ax = plt.subplots()

    # Plot the histogram of correlation values
    # Validate num_bins
    if num_bins <= 0:
        msg = f"Number of bins must be positive, got {num_bins}"
        logger.exception(msg)
        raise ValueError()

    try:
        bin_values, bin_edges, _ = dist_ax.hist(correlation_vals, bins=num_bins)
    except Exception as e:
        msg = f"Error generating histogram: {e}"
        logger.exception(msg)
        raise e

    # Set up axis labels
    dist_ax.set_xlabel(xlabel)
    dist_ax.set_ylabel(ylabel)

    # Set axis bounds
    dist_ax.set_xbound(-1.0, 1.0)
    dist_ax.set_ybound(y_lower_bound, y_upper_bound)

    # Set title and subtitle
    # Suptitle is the super title, which will be above the title
    plt.suptitle(title, fontsize=14)
    plt.title(subtitle, fontsize=10)

    return dist_fig, bin_values, bin_edges