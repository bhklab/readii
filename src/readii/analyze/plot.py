import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from pandas import DataFrame

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