from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from matplotlib.figure import Figure

from readii.io.writers.base_writer import BaseWriter
from readii.utils import logger


class PlotWriterError(Exception):
    """Base exception for PlotWriter errors."""

    pass


class PlotWriterIOError(PlotWriterError):
    """Raised when I/O operations fail."""

    pass

class PlotWriterPlotExistsError(PlotWriterError):
    """Raised when a plot already exists at the specified path."""

    pass

class PlotWriterValidationError(PlotWriterError):
    """Raised when validation of writer configuration fails."""

    pass

@dataclass
class PlotWriter(BaseWriter):
    """Class for managing file writing with customizable paths and filenames for plot figure files."""

    overwrite: bool = field(
        default=False,
        metadata={
            "help": "If True, allows overwriting existing files. If False, raises PlotWriterIOError."
        },
    )
    # Make extensions immutable
    VALID_EXTENSIONS: ClassVar[list[str]] = (
		".png",
		".pdf",
        ".ps",
        ".eps",
        ".svg"
    )

    def __post_init__(self) -> None:
        """Validate writer configuration."""
        super().__post_init__()

        if not any(self.filename_format.endswith(ext) for ext in self.VALID_EXTENSIONS):
            msg = f"Invalid filename format {self.filename_format}. Must end with one of {self.VALID_EXTENSIONS}."
            raise PlotWriterValidationError(msg)

    def save(self, plot:Figure, **kwargs: str) -> Path:
        """Save the plot to a .png file with extra whitespace removed.
        
        Parameters
        ----------
        plot : matplotlib.figure.Figure
            The plot to save.
        kwargs : dict
            Additional keyword arguments to pass to the save method.

        Returns
        -------
        Path
            The path to the saved file.

        Raises
        ------
        PlotWriterIOError
            If there is an error saving the plot.
        PlotWriterValidationError
            If the filename format is invalid.      
        """
        logger.debug("Saving.", kwargs=kwargs)

        # Generate the output path
        out_path = self.resolve_path(**kwargs)

        # Check if the output path already exists
        if out_path.exists():
            if not self.overwrite:
                msg = f"File {out_path} already exists. \nSet {self.__class__.__name__}.overwrite to True to overwrite."
                raise PlotWriterPlotExistsError(msg)
            else:
                logger.warning(f"File {out_path} already exists. Overwriting.")
                
        logger.debug("Saving plot to file", out_path=out_path)
        try:
            # Save the plot to the output path, remove extra whitespace around the figure
            plot.savefig(out_path, bbox_inches='tight')

        except Exception as e:
            msg = f"Error saving plot to file {out_path}: {e}"
            raise PlotWriterIOError(msg) from e
        else:
            logger.info("Plot saved successfully.", out_path=out_path)
            return out_path


if __name__ == "__main__": # pragma: no cover
    from rich import print  # noqa

    plot_writer = PlotWriter(
        root_directory=Path("TRASH", "plot_writer_examples"),
        filename_format="{DatasetName}_{PlotType}_{FeatureType}_{ImageType}_plot.png",
        overwrite=True,
        create_dirs=True
    )

    print(plot_writer)