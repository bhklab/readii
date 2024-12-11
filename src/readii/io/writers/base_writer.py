import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

from imgtools.dicom.sort.exceptions import InvalidPatternError
from imgtools.dicom.sort.parser import PatternParser

from readii.utils import logger


@dataclass
class PatternResolver:
  """Handles parsing and validating filename patterns."""

  DEFAULT_PATTERN: re.Pattern = field(default=re.compile(r"%(\w+)|\{(\w+)\}"), init=False)
  filename_format: str = field(init=True)

  def __init__(self, filename_format: str) -> None:
    self.filename_format = filename_format

    try:
      self.pattern_parser = PatternParser(
        self.filename_format, pattern_parser=self.DEFAULT_PATTERN
      )
      self.formatted_pattern, self.keys = self.parse()  # Validate the pattern by parsing it
    except InvalidPatternError as e:
      msg = f"Invalid filename format: {e}"
      raise ValueError(msg) from e
    else:
      logger.debug("All keys are valid.", pattern=self.formatted_pattern, keys=self.keys)

  def parse(self) -> Tuple[str, list[str]]:
    """
    Parse and validate the pattern.

    Returns
    -------
    Tuple[str, List[str]]
      The formatted pattern string and a list of extracted keys.

    Raises
    ------
    InvalidPatternError
      If the pattern contains no valid placeholders or is invalid.
    """
    return self.pattern_parser.parse()

  def resolve(self, context: Dict[str, Any]) -> str:
    """Resolve the pattern using the provided context dictionary.

    Parameters
    ----------
    context : Dict[str, Any]
      Dictionary containing key-value pairs to substitute in the pattern.

    Returns
    -------
    str
      The resolved pattern string with placeholders replaced by values.

    Raises
    ------
    ValueError
      If a required key is missing from the context dictionary.
    """
    try:
      return self.formatted_pattern % context
    except KeyError as e:
      missing_key = e.args[0]
      valid_keys = ", ".join(context.keys())
      msg = f"Missing value for placeholder '{missing_key}'. Valid keys: {valid_keys}"
      msg += "\nPlease provide a value for this key in the `kwargs` argument,"
      msg += f" i.e `{self.__class__.__name__}.save(..., {missing_key}=value)`."
      raise ValueError(msg) from e

@dataclass
class BaseWriter(ABC):
  """Abstract base class for managing file writing with customizable paths and filenames."""

  # Any subclass has to be initialized with a root directory and a filename format
  root_directory: Path
  filename_format: str

  # optionally, you can set create_dirs to False if you want to handle the directory creation yourself
  create_dirs: bool = field(default=True)

  # subclasses dont need to worry about the pattern_resolver
  pattern_resolver: PatternResolver = field(init=False)

  def __post_init__(self) -> None:
    """Initialize the writer with the given root directory and filename format."""
    self.root_directory = Path(self.root_directory)
    if self.create_dirs:
      self.root_directory.mkdir(parents=True, exist_ok=True)
    elif not self.root_directory.exists():
      msg = f"Root directory {self.root_directory} does not exist."
      raise FileNotFoundError(msg)
    self.pattern_resolver = PatternResolver(self.filename_format)

  @abstractmethod
  def save(self, *args: Any, **kwargs: Any) -> Path:  # noqa
    """Abstract method for writing data. Must be implemented by subclasses."""
    pass

  def _generate_datetime_strings(self) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    return {
      "date": now.strftime("%Y-%m-%d"),
      "time": now.strftime("%H%M%S"),
      "date_time": now.strftime("%Y-%m-%d_%H%M%S"),
    }

  def resolve_path(self, **kwargs: str) -> Path:
    """Generate a file path based on the filename format, subject ID, and additional parameters."""
    context = {**self._generate_datetime_strings(), **kwargs}
    filename = self.pattern_resolver.resolve(context)
    out_path = self.root_directory / filename
    if self.create_dirs:
      out_path.parent.mkdir(parents=True, exist_ok=True)
    return out_path


if __name__ == "__main__":
  from pathlib import Path

  from rich import print  # noqa
  print("-" * 80)
  print("[bold]Example usage[/bold]")
  print("-" * 80)
  print("TEXT WRITER EXAMPLE\n\n")

  # Example subclass for writing text files
  # Define a concrete subclass of BaseWriter that will handle the saving of a specific file type
  # this is a simple example with no validation or error handling
  class TextWriter(BaseWriter): # noqa
    def save(self, content: str, **kwargs: Any) -> Path:  # noqa
      output_path = self.resolve_path(**kwargs)
      with output_path.open('w') as f: # noqa
        f.write(content)
      return output_path

  # Create text writers with different filename patterns
  text_writers = [
    TextWriter(
      root_directory="TRASH/output/text_data",
      filename_format=fmt
    ) for fmt in [
      # a placeholder can be of the format {key} or %key
      "notes_%SubjectID.txt",

      # You define the placeholder that you will later pass in as a keyword argument in the save method
      # By default, the writer automatically has data for the current "date", "time", and "date_time"
      #  so those can be used as placeholders
      "important-file-name_{SubjectID}_{date}.txt",
      "subjects/{SubjectID}/{time}_result.txt",
      "subjects/{SubjectID}_Birthday-{SubjectBirthDate}/data_{date_time}.txt",
    ]
  ]

  # Define some example data to pass to the writers
  # this could be extracted from some data source and used to generate the file names
  SubjectID="SUBJ001"
  SubjectBirthDate="2022-01-01"

  # Test text writers
  for writer in text_writers:
    path = writer.save(
      content = "Sample text content", # this is the data that will be written to the file

      # They key-value pairs can be passed in as keyword arguments, and matched to placeholders in the filename format
      SubjectID=SubjectID, 
      SubjectBirthDate=SubjectBirthDate,

      # If you pass in a key that is not in the filename format, it will be ignored
      # this can also be seen as `SubjectBirthDate` is only used in one of the above filename formats
      RandomKey="This will be ignored",
      RandomKey2="This will also be ignored"
    )
    print(f"{writer.__class__.__name__} with format [magenta]'{writer.pattern_resolver.formatted_pattern}':")
    print(f"File written to: [green]{path}\n")

  print("-" * 80)

  subject_data_examples = [
    {
      "PatientID": f"PAT{i:03d}",
      "Modality": f"{modality}",
      "Study": f"Study{j:03d}",
      "DataType": f"{data_type}",
    }
    for i in range(1, 4)
    for j in range(1, 3)
    for modality in ["CT", "RTSTRUCT"]
    for data_type in ["raw", "processed", "segmented", "labeled"]
  ]

  print("CSV WRITER EXAMPLE\n\n")
  # Example subclass for writing CSV files
  import pandas as pd
  class CSVWriter(BaseWriter): # noqa
    def save(self, data: list, **kwargs: Any) -> Path:  # noqa
      output_path = self.resolve_path(**kwargs)
      with output_path.open('w') as f: # noqa
        pd.DataFrame(data).to_csv(f, index=False)
      return output_path

  # Create CSV writers with different filename patterns
  csv_writer = CSVWriter(
    root_directory="TRASH/output/patient_data",
    filename_format="PatientID-{PatientID}/Study-{Study}/{Modality}/{DataType}-data.csv"
  )

  # Test CSV writers
  for patient in subject_data_examples:
    path = csv_writer.save(
      data = pd.DataFrame(patient, index=[0]), # just assume that this dataframe is some real data
      PatientID=patient["PatientID"],
      Study=patient["Study"],
      Modality=patient["Modality"],
      DataType=patient["DataType"]
    )
  
  # run the tree command and capture the output
  import subprocess
  output = subprocess.check_output(["tree", "-F", "TRASH/output/patient_data"])
  print(output.decode("utf-8"))

