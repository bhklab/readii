from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

from readii.io.writers.base_writer import BaseWriter
from readii.utils import logger

class PlotWriterError(Exception):
    """Base exception for PlotWriter errors."""

    pass


class PlotWriterIOError(PlotWriterError):
    """Raised when I/O operations fail."""

    pass

@dataclass
class PlotWriter(BaseWriter):
    """Class for managing file writing with customizable paths and filenames for plot figure files."""

    overwrite: bool = field(
        default=False,
        metadata={
            "help": "If True, allows overwriting existing files. If False, raises FileExistsError."
        },
    )

    def save(self, plot:matplotlib.figure.Figure, **kwargs: str) -> Path:
        """Save the plot to a .png file."""

        logger.debug("Saving.", kwargs=kwargs)

        # Generate the output path
        out_path = self.resolve_path(**kwargs)

        # Check if the output path already exists
        if out_path.exists():
            if not self.overwrite:
                msg = f"File {out_path} already exists. \nSet {self.__class__.__name__}.overwrite to True to overwrite."
                logger.exception(msg)
                raise FileExistsError(msg)
            else:
                logger.warning(f"File {out_path} already exists. Overwriting.")
                
        logger.debug("Saving plot to file", out_path=out_path)
        try:
            # Save the plot to the output path, remove extra whitespace around the figure
            plot.savefig(out_path, bbox_inches='tight')

        except Exception as e:
            msg = f"Error saving plot to file {out_path}: {e}"
            logger.exception(msg)
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