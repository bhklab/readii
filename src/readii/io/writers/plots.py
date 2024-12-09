from seaborn import heatmap
import os

from typing import Union
from pathlib import Path

def saveSeabornPlotFigure(sns_plot:heatmap,
                          plot_name:str,
                          output_dir_path:Union[Path|str]
                          ):
    """Function to save out a seaborn plot to a png file.

    Parameters
    ----------
    sns_plot : seaborn.heatmap
        Seaborn plot to save out.
    plot_name : str
        What to name the plot on save. Ex. "original_vs_shuffled_correlation_plot.png"
    output_dir_path : str
        Path to the directory to save the plot to.

    """

    # Check if output_dir_path is a string or a Path object
    if isinstance(output_dir_path, str):
        output_dir_path = Path(output_dir_path)
    
    # Check if output_dir_path exists
    if not output_dir_path.exists():
        # Make directory if it doesn't exist, but don't fail if it already exists
        os.makedirs(output_dir_path, exist_ok=True)
    
    # Set up the full output path
    output_file_path = output_dir_path / plot_name

    # Save out the plot
    sns_plot.get_figure().savefig(output_file_path, bbox_inches='tight')

    return