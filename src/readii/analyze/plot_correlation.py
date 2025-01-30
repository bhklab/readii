from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from scipy.linalg import issymmetric

from readii.analyze.correlation import getCrossCorrelations, getSelfCorrelations
from readii.io.writers.plot_writer import PlotWriter, PlotWriterPlotExistsError
from readii.utils import logger


def saveCorrelationHeatmap(plot_figure:Figure,
                           correlation_directory:Path,
                           cmap:str,
                           feature_types:list[str],
                           correlation_type:str,
                           overwrite:bool = False) -> Path:
    """Save a heatmap figure to a file with a PlotWriter.

    Parameters
    ----------
    plot_figure : matplotlib.figure.Figure
        The plot to save.
    correlation_directory : pathlib.Path
        The directory to save the heatmap to.
    cmap : str
        The colormap used for the heatmap.
    feature_types : list[str]
        The feature types on the x and y axes of the heatmap. Cross correlatins will be concatenated with "_vs_" to create the title.
    correlation_type : str
        The correlation method + type used for the heatmap. For example, "pearson_self".
    overwrite : bool, optional
        Whether to overwrite an existing file. The default is False.

    Returns
    -------
    Path
        The path to the saved file.
        
    Example
    -------
    >>> saveCorrelationHeatmap(corr_fig,
                                correlation_directory=Path("correlations"),
                                cmap="nipy_spectral",
                                feature_types=["vertical", "horizontal"],
                                correlation_type="pearson_cross")

    File will be saved to correlations/heatmap/nipy_spectral/vertical_vs_horizontal_pearson_cross_correlation_heatmap.png
    """
    # Set up the writer
    corr_heatmap_writer = PlotWriter(root_directory = correlation_directory,
                                     filename_format = "heatmap/{ColorMap}/{FeaturesPlotted}_{CorrelationType}_correlation_heatmap.png",
                                     overwrite = overwrite,
                                     create_dirs = True)
    
    # Turn feature types into a string
    # Single feature type will be in the form "feature_type"
    # Multiple feature types will be in the form "feature_type_vs_feature_type"
    feature_type_str = "_vs_".join(feature_types)

    # Save the heatmap
    try:
        return corr_heatmap_writer.save(plot_figure,
                                        ColorMap=cmap,
                                        FeaturesPlotted=feature_type_str,
                                        CorrelationType=correlation_type)
     
    except PlotWriterPlotExistsError as e:
        logger.warning(e)
    
        # If plot file already exists, return the path to the existing plot
        return corr_heatmap_writer.resolve_path(ColorMap=cmap,
                                                FeaturesPlotted=feature_type_str,
                                                CorrelationType=correlation_type)



def saveCorrelationHistogram(plot_figure:Figure,
                             correlation_directory:Path,
                             feature_types:list[str],
                             correlation_type:str,
                             overwrite:bool = False) -> Path:
    """Save a histogram figure to a file with a PlotWriter.

    Parameters
    ----------
    plot_figure : matplotlib.figure.Figure
        The plot to save.
    correlation_directory : pathlib.Path
        The directory to save the heatmap to.
    feature_types : list[str]
        The feature types from the correlation matrix used for the histogram. Cross correlatins will be concatenated with "_vs_" to create the title.
    correlation_type : str
        The correlation method + type used for the heatmap. For example, "pearson_self".
    overwrite : bool, optional
        Whether to overwrite an existing file. The default is False.

    Returns
    -------
    Path
        The path to the saved file.
        
    Example
    -------
    >>> saveCorrelationHistogram(corr_fig,
                                 correlation_directory=Path("correlations"),
                                 feature_types=["vertical", "horizontal"],
                                 correlation_type="pearson_cross")

    File will be saved to correlations/histogram/vertical_vs_horizontal_pearson_cross_correlation_histogram.png
    """
    corr_histogram_writer = PlotWriter(root_directory = correlation_directory,
                                       filename_format= "histogram/{FeaturesPlotted}_{CorrelationType}_correlation_histogram.png",
                                       overwrite=overwrite,
                                       create_dirs=True)
    
    # Turn feature types into a string
    # Single feature type will be in the form "feature_type"
    # Multiple feature types will be in the form "feature_type_vs_feature_type"
    feature_type_str = "_vs_".join(feature_types)

    # Save the heatmap
    try:
        return corr_histogram_writer.save(plot_figure,
                                          FeaturesPlotted=feature_type_str,
                                          CorrelationType=correlation_type)
    except PlotWriterPlotExistsError as e:
        logger.warning(e)

        # If plot file already exists, return the path to the existing plot
        return corr_histogram_writer.resolve_path(FeaturesPlotted=feature_type_str,
                                                  CorrelationType=correlation_type)



def plotCorrelationHeatmap(correlation_matrix_df:pd.DataFrame,
                           diagonal:bool = False,
                           triangle:Optional[str] = "lower",
                           cmap:str = "nipy_spectral",
                           xlabel:str = "",
                           ylabel:Optional[str] = "",
                           title:Optional[str] = "",
                           subtitle:Optional[str] = "",
                           show_tick_labels:bool = False) -> Figure:
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
                             ) -> tuple[Figure, np.ndarray, np.ndarray]:
    """Plot a histogram to show the distribution of correlation values for a correlation matrix.

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


########################################################################################################################
################################## SELF AND CROSS CORRELATION HEATMAPS##################################################
########################################################################################################################
def plotSelfCorrHeatmap(correlation_matrix:pd.DataFrame,
                        feature_type_name:str,
                        correlation_method:str = "pearson",
                        cmap:str='nipy_spectral',
                        save_dir_path:Optional[str] = None,
                        overwrite:bool = False) -> tuple[Figure | Figure, Path]:
    """Plot a heatmap of the self correlations from a correlation matrix.
    
    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    feature_type_name : str
        Name of the feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix.
    correlation_method : str, optional
        Method to use for calculating correlations. Default is "pearson".
    cmap : str, optional
        Colormap to use for the heatmap. Default is "nipy_spectral".
    save_dir_path : str, optional
        Path to save the heatmap to. If None, the heatmap will not be saved. Default is None.
        File will be saved to {save_dir_path}/heatmap/{cmap}/{feature_type_name}_{correlation_method}_self_correlation_heatmap.png
    
    Returns
    -------
    self_corr_heatmap : matplotlib.pyplot.figure
        Figure object containing the heatmap of the self correlations.
    if save_path is not None:
        self_corr_save_path : Path
            Path to the saved heatmap.
    """
    # Get the self correlations for the specified feature type
    self_corr = getSelfCorrelations(correlation_matrix, feature_type_name)

    # Make the heatmap figure
    self_corr_heatmap = plotCorrelationHeatmap(self_corr, 
                                               diagonal=True, 
                                                cmap=cmap, 
                                                xlabel=feature_type_name, 
                                                ylabel=feature_type_name,
                                                title=f"{correlation_method.capitalize()} Self Correlations", 
                                                subtitle=f"{feature_type_name}")

    if save_dir_path is not None:
        # Save the heatmap to a png file
        self_corr_save_path = saveCorrelationHeatmap(self_corr_heatmap,
                                                     save_dir_path,
                                                     cmap=cmap,
                                                     feature_types=[feature_type_name],
                                                     correlation_type=f"{correlation_method}_self",
                                                     overwrite=overwrite)
        # Return the figure and path to the saved heatmap
        return self_corr_heatmap, self_corr_save_path

    else:
        # Return the figure without saving
        return self_corr_heatmap



def plotCrossCorrHeatmap(correlation_matrix:pd.DataFrame,
                         vertical_feature_name:str,
                         horizontal_feature_name:str,
                         correlation_method:str = "pearson",
                         cmap:str='nipy_spectral',
                         save_dir_path:Optional[str] = None,
                         overwrite:bool = False) -> tuple[Figure | Figure, Path]:
    """Plot a heatmap of the cross correlations from a correlation matrix.
    
    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    vertical_feature_name : str
        Name of the vertical feature to get cross correlations for. Must be the suffix of some feature names in the correlation matrix index.
    horizontal_feature_name : str
        Name of the horizontal feature to get cross correlations for. Must be the suffix of some feature names in the correlation matrix columns.
    correlation_method : str, optional
        Method to use for calculating correlations. Default is "pearson".
    cmap : str, optional
        Colormap to use for the heatmap. Default is "nipy_spectral".
    save_dir_path : str, optional
        Path to save the heatmap to. If None, the heatmap will not be saved. Default is None.
        File will be saved to {save_dir_path}/heatmap/{cmap}/{vertical_feature_name}_vs_{horizontal_feature_name}_{correlation_method}_cross_correlation_heatmap.png
    overwrite : bool, optional
        Whether to overwrite an existing plot figure file. The default is False.
        
    Returns
    -------
    cross_corr_heatmap : matplotlib.pyplot.figure
        Figure object containing the heatmap of the cross correlations.
    if save_path is not None:
        cross_corr_save_path : Path
            Path to the saved heatmap.
    """
    # Get the cross correlations for the specified feature type
    cross_corr = getCrossCorrelations(correlation_matrix, vertical_feature_name, horizontal_feature_name)

    # Make the heatmap figure
    cross_corr_heatmap = plotCorrelationHeatmap(cross_corr, 
                                                diagonal=False, 
                                                cmap=cmap, 
                                                xlabel=horizontal_feature_name, 
                                                ylabel=vertical_feature_name,
                                                title=f"{correlation_method.capitalize()} Cross Correlations", 
                                                subtitle=f"{vertical_feature_name} vs {horizontal_feature_name}")
    
    if save_dir_path is not None:
        # Save the heatmap to a png file
        cross_corr_save_path = saveCorrelationHeatmap(cross_corr_heatmap,
                                                      save_dir_path,
                                                      cmap=cmap,
                                                      feature_types=[vertical_feature_name, horizontal_feature_name],
                                                      correlation_type=f"{correlation_method}_cross",
                                                      overwrite=overwrite)
        # Return the figure and the path to the saved heatmap 
        return cross_corr_heatmap, cross_corr_save_path
        
    else:
        # Return the heatmap figure
        return cross_corr_heatmap
    

########################################################################################################################
################################## SELF AND CROSS CORRELATION HISTOGRAMS ###############################################
########################################################################################################################

def plotSelfCorrHistogram(correlation_matrix:pd.DataFrame,
                          feature_type_name:str,
                          correlation_method:str = "pearson",
                          num_bins:int = 100,
                          y_lower_bound:int = 0,
                          y_upper_bound:int = None,
                          save_dir_path:Optional[str] = None,
                          overwrite:bool = False) -> tuple[Figure | Figure, Path]:
    """Plot a histogram of the self correlations from a correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    feature_type_name : str
        Name of the feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix.
    correlation_method : str, optional
        Method to use for calculating correlations. Default is "pearson".
    num_bins : int, optional
        Number of bins to use for the histogram generation. The default is 100.
    y_lower_bound : int, optional
        Lower bound for the y-axis of the histogram. The default is 0.
    y_upper_bound : int, optional
        Upper bound for the y-axis of the histogram. The default is None.
    save_dir_path : str, optional
        Path to save the histogram to. If None, the histogram will not be saved. Default is None.
        File will be saved to {save_dir_path}/histogram/{feature_type_name}_{correlation_method}_self_correlation_histogram.png
    overwrite : bool, optional
        Whether to overwrite an existing plot figure file. The default is False.
        
    Returns
    -------
    self_corr_hist : plt.Figure
        Figure object containing the histogram of the self correlations.
    if save_dir_path is not None:
        self_corr_save_path : Path
            Path to the saved histogram.
    """
    # Get the self correlations for the specified feature type
    self_corr = getSelfCorrelations(correlation_matrix, feature_type_name)

    # Make the histogram figure
    self_corr_hist, _, _ = plotCorrelationHistogram(self_corr,
                                                    num_bins=num_bins,
                                                    xlabel = f"{correlation_method.capitalize()} Self Correlations",
                                                    y_lower_bound = y_lower_bound,
                                                    y_upper_bound = y_upper_bound,
                                                    title = f"Distribution of {correlation_method.capitalize()} Self Correlations",
                                                    subtitle = f"{feature_type_name}")
    
    if save_dir_path is not None:
        # Save the histogram to a png file
        self_corr_save_path = saveCorrelationHistogram(self_corr_hist,
                                                       save_dir_path,
                                                       feature_types=[feature_type_name],
                                                       correlation_type=f"{correlation_method}_self",
                                                       overwrite=overwrite)

        # Return the figure and the path to the saved histogram 
        return self_corr_hist, self_corr_save_path
        
    else:
        # Return the histogram figure
        return self_corr_hist



def plotCrossCorrHistogram(correlation_matrix:pd.DataFrame,
                           vertical_feature_name:str,
                           horizontal_feature_name:str,
                           correlation_method:str = "pearson",
                           num_bins:int = 100,
                           y_lower_bound:int = 0,
                           y_upper_bound:int = None,
                           save_dir_path:Optional[str] = None,
                           overwrite:bool = False) -> tuple[Figure | Figure, Path]:
    """Plot a histogram of the cross correlations from a correlation matrix.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Dataframe containing the correlation matrix to plot.
    vertical_feature_name : str
        Name of the vertical feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix index.
    horizontal_feature_name : str
        Name of the horizontal feature type to get self correlations for. Must be the suffix of some feature names in the correlation matrix columns.
    correlation_method : str, optional
        Method to use for calculating correlations. Default is "pearson".
    num_bins : int, optional
        Number of bins to use for the histogram generation. The default is 100.
    y_lower_bound : int, optional
        Lower bound for the y-axis of the histogram. The default is 0.
    y_upper_bound : int, optional
        Upper bound for the y-axis of the histogram. The default is None.
    save_dir_path : str, optional
        Path to save the histogram to. If None, the histogram will not be saved. Default is None.
        File will be saved to {save_dir_path}/histogram/{vertical_feature_name}_vs_{horizontal_feature_name}_{correlation_method}_cross_correlation_histogram.png
    overwrite : bool, optional
        Whether to overwrite an existing plot figure file. The default is False.
    
    Returns
    -------
    cross_corr_hist : plt.Figure
        Figure object containing the histogram of the cross correlations.
    if save_dir_path is not None:
        cross_corr_save_path : Path
            Path to the saved histogram.
    """
    # Get the cross correlations for the specified feature type
    cross_corr = getCrossCorrelations(correlation_matrix, vertical_feature_name, horizontal_feature_name)

    # Make the histogram figure
    cross_corr_hist, _, _ = plotCorrelationHistogram(cross_corr, 
                                               num_bins=num_bins,
                                               xlabel = f"{correlation_method.capitalize()} Correlation",
                                               y_lower_bound = y_lower_bound,
                                               y_upper_bound = y_upper_bound,
                                               title = f"Distribution of {correlation_method.capitalize()} Cross Correlations",
                                               subtitle=f"{vertical_feature_name} vs {horizontal_feature_name}")
    
    if save_dir_path is not None:
        # Save the histogram to a png file
        cross_corr_save_path = saveCorrelationHistogram(cross_corr_hist,
                                                        save_dir_path,
                                                        feature_types=[vertical_feature_name, horizontal_feature_name],
                                                        correlation_type=f"{correlation_method}_cross",
                                                        overwrite=overwrite)
        
        # Return the figure and the path to the saved histogram 
        return cross_corr_hist, cross_corr_save_path

    else:
        # Return the histogram figure
        return cross_corr_hist