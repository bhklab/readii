import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.linalg import issymmetric
from pandas import DataFrame

from .correlation import (
    getVerticalSelfCorrelations, 
    getHorizontalSelfCorrelations, 
    getCrossCorrelationMatrix 
)

def plotCorrelationHeatmap(correlation_matrix_df:DataFrame,
                           diagonal:bool = False,
                           triangle:str = "lower",
                           cmap:str = "nipy_spectral",
                           xlabel:str = "",
                           ylabel:str = "",
                           title:str = "",
                           subtitle:str = "",
                           show_tick_labels:bool = False
                           ):
    """Function to plot a correlation heatmap and return the figure object.

    Parameters
    ----------
    correlation_matrix_df : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    diagonal : bool, 
        Whether to only plot half of the matrix. The default is False.
    triangle : str, 
        Which triangle half of the matrixto plot. The default is "lower".
    xlabel : str, 
        Label for the x-axis. The default is "".
    ylabel : str, 
        Label for the y-axis. The default is "".
    title : str, 
        Title for the plot. The default is "".
    subtitle : str, 
        Subtitle for the plot. The default is "".
    show_tick_labels : bool, 
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



def plotSelfCorrelationHeatMaps(correlation_matrix:DataFrame,
                                axis:str,
                                num_axis_features:int,
                                feature_name:str,
                                correlation_method:str = "",
                                extraction_method:str = "",
                                dataset_name:str = "",
                                cmap:str = "nipy_spectral",
                                ):
    """ Function to plot a correlation heatmap for the vertical (y-axis) and horizontal (x-axis) self correlations.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    axis : str
        Axis to plot the self correlations for. Must be either "vertical" or "horizontal". The default is "vertical".
    num_axis_features : int
        Number of features in the axis to plot the self correlations for. This is used to get the self correlations from the correlation matrix.
    feature_name : str
        Name of the feature to use for the plot title and subtitle.
    correlation_method : str, optional
        Name of the correlation method to use for the plot title and subtitle. The default is "".
    extraction_method : str, optional
        Name of the extraction method to use for the plot title and subtitle. The default is "".
    dataset_name : str, optional
        Name of the dataset to use for the plot title and subtitle. The default is "".
    cmap : str, optional
        Name of the matplotlib colormap to use for the heatmap. The default is "nipy_spectral".

    Returns
    -------
    self_plot : matplotlib.pyplot.figure
        Figure object containing a Seaborn heatmap of the vertical or horizontalself correlations from the correlation matrix.
    """

    if axis == "vertical":
        # Get the correlation matrix for vertical vs vertical
        # This is the top left corner of the matrix
        self_correlations = getVerticalSelfCorrelations(correlation_matrix, num_axis_features)
    elif axis == "horizontal":
        # Get the correlation matrix for horizontal vs horizontal
        # This is the bottom right corner of the matrix
        self_correlations = getHorizontalSelfCorrelations(correlation_matrix, num_axis_features)
    else:
        raise ValueError(f"Axis must be either 'vertical' or 'horizontal'. Provided axis is {axis}.")

    # Create correlation heatmap for vertical vs vertical
    self_plot = plotCorrelationHeatmap(self_correlations,
                                       diagonal = True,
                                       triangle = "lower",
                                       cmap = cmap,
                                       xlabel = feature_name,
                                       ylabel = feature_name,
                                       title = f"{correlation_method.capitalize()} Self Correlations for {dataset_name} {extraction_method.capitalize()} Features",
                                       subtitle = f"{feature_name} vs. {feature_name}")

    return self_plot



def plotCrossCorrelationHeatmap(correlation_matrix:DataFrame,
                                num_vertical_features:int,
                                vertical_feature_name:str,
                                horizontal_feature_name:str,
                                correlation_method:str = "",
                                extraction_method:str = "",
                                dataset_name:str = "",
                                cmap:str = "nipy_spectral"):
    """ Function to plot heatmap for a the cross-correlation section of a correlation matrix. Will be the top right quadrant of the correlation matrix so vertical and horizontal features are correctly labeled.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    num_vertical_features : int
        Number of vertical (y-axis) features in the correlation matrix.
        The number of vertical features must be less than the number of rows in the correlation matrix.
    vertical_feature_name : str
        Name of the vertical feature to use for the plot title and subtitle.
    horizontal_feature_name : str
        Name of the horizontal feature to use for the plot title and subtitle.
    correlation_method : str, optional
        Name of the correlation method to use for the plot title and subtitle. The default is "".
    extraction_method : str, optional
        Name of the extraction method to use for the plot title and subtitle. The default is "".
    dataset_name : str, optional
        Name of the dataset to use for the plot title and subtitle. The default is "".
    cmap : str, optional
        Name of the matplotlib colormap to use for the heatmap. The default is "nipy_spectral".
    
    Returns
    -------
    cross_corr_plot : matplotlib.pyplot.figure
        Figure object containing a Seaborn heatmap of the cross correlations from the correlation matrix.
    """
    
    # Get the cross correlation matrix from the main correlation matrix
    cross_corr_matrix = getCrossCorrelationMatrix(correlation_matrix, num_vertical_features)

    # Create heatmap for the cross correlation matrix
    cross_corr_plot = plotCorrelationHeatmap(cross_corr_matrix,
                                             diagonal = False,
                                             cmap=cmap,
                                             xlabel = horizontal_feature_name,
                                             ylabel = vertical_feature_name,
                                             title = f"{correlation_method.capitalize()} Cross Correlations for {dataset_name} {extraction_method.capitalize()} Features",
                                             subtitle = f"{vertical_feature_name} vs. {horizontal_feature_name}")

    return cross_corr_plot



def plotCorrelationDistribution(correlation_matrix:DataFrame,
                                num_bins:int = 100,
                                xlabel:str = "Correlations",
                                ylabel:str = "Frequency",
                                y_lower_bound:int = 0,
                                y_upper_bound:int = None,
                                title:str = "Distribution of Correlations for Features",
                                subtitle:str = "",
                                ):
    """ Function to plot a distribution of correlation values for a correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    num_bins : int, 
        Number of bins to use for the distribution plot. The default is 100.
    xlabel : str, 
        Label for the x-axis. The default is "Correlations".
    ylabel : str, 
        Label for the y-axis. The default is "Frequency".
    y_lower_bound : int, 
        Lower bound for the y-axis of the distribution plot. The default is 0.
    y_upper_bound : int, 
        Upper bound for the y-axis of the distribution plot. The default is None.
    title : str, 
        Title for the plot. The default is "Distribution of Correlations for Features".
    subtitle : str, 
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
        print("Correlation matrix is symmetric.")
        # Get only the bottom left triangle of the correlation matrix since the matrix is symmetric 
        lower_half_idx = np.mask_indices(feature_correlation_arr.shape[0], np.tril)
        # This is a 1D array for binning and plotting
        correlation_vals = feature_correlation_arr[lower_half_idx]
    else:
        # Flatten the matrix to a 1D array for binning and plotting
        correlation_vals = feature_correlation_arr.flatten()

    dist_fig, dist_ax = plt.subplots()
    bin_values, bin_edges, _ = dist_ax.hist(correlation_vals, bins=num_bins)
    dist_ax.set_xlabel(xlabel)
    dist_ax.set_ylabel(ylabel)
    dist_ax.set_xbound(-1.0, 1.0)
    dist_ax.set_ybound(y_lower_bound, y_upper_bound)
    plt.suptitle(title, fontsize=14)
    plt.title(subtitle, fontsize=10)

    return dist_fig, bin_values, bin_edges



def plotSelfCorrelationDistributionPlots(correlation_matrix:DataFrame,
                                         axis:str,
                                         num_axis_features:int,
                                         feature_name:str,
                                         num_bins: int = 450,
                                         y_upper_bound:int = None,
                                         correlation_method:str = "",
                                         extraction_method:str = "",
                                         dataset_name:str = "",
                                         ):
    """ Function to plot a distribution of self correlation values for a correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    axis : str
        Axis to plot the self correlations for. Must be either "vertical" or "horizontal".
    num_axis_features : int
        Number of features in the axis to plot the self correlations for. This is used to get the self correlations from the correlation matrix.
    feature_name : str
        Name of the feature to use for the plot title and subtitle.
    num_bins : int, optional
        Number of bins to use for the distribution plot. The default is 450.
    y_upper_bound : int, optional
        Upper bound for the y-axis of the distribution plot. The default is None.
    correlation_method : str, optional
        Name of the correlation method to use for the plot title and subtitle. The default is "".
    extraction_method : str, optional
        Name of the extraction method to use for the plot title and subtitle. The default is "".
    dataset_name : str, optional
        Name of the dataset to use for the plot title and subtitle. The default is "".

    Returns
    -------
    self_corr_dist_fig : plt.Figure
        Figure object containing the histogram of self correlation values.
    """
    
    if axis == "vertical":
        # Get the correlation matrix for vertical vs vertical
        # This is the top left corner of the matrix
        self_correlations = getVerticalSelfCorrelations(correlation_matrix, num_axis_features)
    elif axis == "horizontal":
        # Get the correlation matrix for horizontal vs horizontal
        # This is the bottom right corner of the matrix
        self_correlations = getHorizontalSelfCorrelations(correlation_matrix, num_axis_features)
    else:
        raise ValueError(f"Axis must be either 'vertical' or 'horizontal'. Provided axis is {axis}.")
    
    # Plot the distribution of correlation values for the self correlations
    self_corr_dist_fig, _, _ = plotCorrelationDistribution(self_correlations,
                                                               num_bins = num_bins,
                                                               xlabel = f"{correlation_method.capitalize()} Correlation",
                                                               ylabel = "Frequency",
                                                               y_upper_bound=y_upper_bound,
                                                               title = f"Distribution of {correlation_method.capitalize()} Self Correlations for {dataset_name} {extraction_method.capitalize()} Features",
                                                               subtitle = f"{feature_name} vs. {feature_name}"
                                                               )
                                                                                                     
    return self_corr_dist_fig



def plotCrossCorrelationDistributionPlots(correlation_matrix:DataFrame,
                                          num_vertical_features:int,
                                          vertical_feature_name:str,
                                          horizontal_feature_name:str,
                                          num_bins: int = 450,
                                          y_upper_bound:int = None,
                                          correlation_method:str = "",
                                          extraction_method:str = "",
                                          dataset_name:str = "",
                                          ):
    """ Function to plot a distribution of cross correlation values for a correlation matrix. Will be the top right quadrant of the correlation matrix so vertical and horizontal features are correctly labeled.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    num_vertical_features : int
        Number of vertical (y-axis) features in the correlation matrix.
        The number of vertical features must be less than the number of rows and columns in the correlation matrix.
    vertical_feature_name : str
        Name of the vertical feature to use for the plot title and subtitle.
    horizontal_feature_name : str
        Name of the horizontal feature to use for the plot title and subtitle.
    num_bins : int, optional
        Number of bins to use for the distribution plot. The default is 450.
    y_upper_bound : int, optional
        Upper bound for the y-axis of the distribution plot. The default is None.
    correlation_method : str, optional
        Name of the correlation method to use for the plot title and subtitle. The default is "".
    extraction_method : str, optional
        Name of the extraction method to use for the plot title and subtitle. The default is "".
    dataset_name : str, optional
        Name of the dataset to use for the plot title and subtitle. The default is "".

    Returns
    -------
    cross_corr_dist_fig : plt.Figure
        Figure object containing the histogram of cross correlation values.
    """
    
    # Get the cross correlation matrix from the main correlation matrix
    cross_corr_matrix = getCrossCorrelationMatrix(correlation_matrix, num_vertical_features)

    # Create heatmap for the cross correlation matrix
    cross_corr_dist_fig, _, _ = plotCorrelationDistribution(cross_corr_matrix,
                                                      num_bins = num_bins,
                                                      xlabel = f"{correlation_method.capitalize()} Correlation",
                                                      ylabel = "Frequency",
                                                      y_upper_bound = y_upper_bound,
                                                      title = f"Distribution of {correlation_method.capitalize()} Cross Correlations for {dataset_name} {extraction_method.capitalize()} Features",
                                                      subtitle = f"{vertical_feature_name} vs. {horizontal_feature_name}"
                                                      )

    return cross_corr_dist_fig