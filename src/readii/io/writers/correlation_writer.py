from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from pandas import DataFrame

from readii.io.writers.base_writer import BaseWriter
from readii.utils import logger


class CorrelationWriterError(Exception):
    """Base exception for CorrelationWriter errors."""

    pass


class CorrelationWriterIOError(CorrelationWriterError):
    """Raised when I/O operations fail."""

    pass


class CorrelationWriterFileExistsError(CorrelationWriterIOError):
    """Raised when a file already exists at the specified path."""

    pass


class CorrelationWriterValidationError(CorrelationWriterError):
    """Raised when validation of writer configuration fails."""

    pass

@dataclass
class CorrelationWriter(BaseWriter):
    """Class for managing file writing with customizable paths and filenames for plot figure files."""

    overwrite: bool = field(
        default=False,
        metadata={
            "help": "If True, allows overwriting existing files. If False, raises CorrelationWriterIOError."
        },
    )

    # Make extensions immutable
    VALID_EXTENSIONS: ClassVar[list[str]] = (
		".csv",
        ".xlsx"
    )

    def __post_init__(self) -> None:
        """Validate writer configuration."""
        super().__post_init__()

        if not any(self.filename_format.endswith(ext) for ext in self.VALID_EXTENSIONS):
            msg = f"Invalid filename format {self.filename_format}. Must end with one of {self.VALID_EXTENSIONS}."
            raise CorrelationWriterValidationError(msg)
        
    def save(self, correlation_df:DataFrame, **kwargs: str) -> Path:
        """Save the correlation dataframe to a .csv file.
        
        Parameters
        ----------
        correlation_df : DataFrame
            The correlation dataframe to save.
        **kwargs : str
            Additional keyword arguments to pass to the filename format.

        Returns
        -------
        Path
            The path to the saved file.
        
        Raises
        ------
        CorrelationWriterIOError
            If an error occurs during file writing.
        CorrelationWriterValidationError
            If the filename format is invalid.
        """
        logger.debug("Saving.", kwargs=kwargs)

        # Generate the output path
        out_path = self.resolve_path(**kwargs)

        # Check if the output path already exists
        if out_path.exists():
            if not self.overwrite:
                msg = f"File {out_path} already exists. \nSet {self.__class__.__name__}.overwrite to True to overwrite."
                raise CorrelationWriterFileExistsError(msg)
            else:
                logger.warning(f"File {out_path} already exists. Overwriting.")
        
        # Check if the correlation dataframe is a DataFrame
        if not isinstance(correlation_df, DataFrame):
            msg = f"Correlation dataframe must be a pandas DataFrame, got {type(correlation_df)}"
            raise CorrelationWriterValidationError(msg)
        
        # Check if the correlation dataframe is empty
        if correlation_df.empty:
            msg = "Correlation dataframe is empty"
            raise CorrelationWriterValidationError(msg)
        
        # Check that the columns and index of the correlation dataframe are the same
        if not correlation_df.columns.equals(correlation_df.index):
            msg = "Correlation dataframe columns and index are not the same"
            raise CorrelationWriterValidationError(msg)

        logger.debug("Saving correlation dataframe to file", out_path=out_path)
        try:
            match out_path.suffix:
                case ".csv":
                    correlation_df.to_csv(out_path, index=True, index_label="")
                case ".xlsx":
                    correlation_df.to_excel(out_path, index=True, index_label="")
                case _:
                    msg = f"Invalid file extension {out_path.suffix}. Must be one of {self.VALID_EXTENSIONS}."
                    raise CorrelationWriterValidationError(msg)
        except Exception as e:
            msg = f"Error saving correlation dataframe to file {out_path}: {e}"
            raise CorrelationWriterIOError(msg) from e
        else:
            logger.info("Correlation dataframe saved successfully.", out_path=out_path)
            return out_path
        

if __name__ == "__main__": # pragma: no cover
    from rich import print  # noqa

    plot_writer = CorrelationWriter(
        root_directory=Path("TRASH", "correlation_writer_examples"),
        filename_format="{DatasetName}_{VerticalFeatureType}_{HorizontalFeatureType}_{CorrelationType}_correlations.csv",
        overwrite=True,
        create_dirs=True
    )

    print(plot_writer)