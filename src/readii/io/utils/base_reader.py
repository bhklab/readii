from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from readii.io.utils.directory_scanner import DirectoryScanner
from readii.io.utils.file_filter import FileDict, FileFilter, FilteredFiles
from readii.io.utils.pattern_resolver import PatternResolver
from readii.utils import logger


@dataclass
class BaseReader:
  """Base class for reading files based on a pattern and extracting metadata.

  Parameters
  ----------
  root_directory : str | Path
      Directory to scan for files.
  filename_pattern : str
      Pattern to match filenames.
  show_warnings : bool, optional
      Whether to show warnings when a file is not matched. Default is False.
  **kwargs : Any
      Additional keyword arguments to pass to DirectoryScanner.
  """

  root_directory: str | Path  # Directory to scan for files
  filename_pattern: str  # Pattern to match filenames
  pattern_resolver: PatternResolver
  directory_scanner: DirectoryScanner
  file_filter: FileFilter
  show_warnings: bool = False

  mapped_files: List[FileDict] = field(default_factory=list)

  def __init__(self, root_directory: str | Path, filename_pattern: str, **kwargs: Any) -> None:  # noqa: ANN401
    self.root_directory = Path(root_directory)
    assert self.root_directory.exists(), f"Root directory {self.root_directory} does not exist."

    self.filename_pattern = filename_pattern
    self.pattern_resolver = PatternResolver(self.filename_pattern)

    self.show_warnings = kwargs.pop("show_warnings", False)

    self.directory_scanner = DirectoryScanner(self.root_directory, **kwargs)
    self.mapped_files = []  # Initialize mapped_files

  def locate_files(self) -> List[Path]:
    """Locate files in the directory that match the filename pattern.
 
    Returns
    -------
    List[Path]
        List of file paths that match the pattern.
    """
    return self.directory_scanner.scan()

  def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
    """Extract metadata from the file path based on the pattern.

    Parameters
    ----------
    file_path : Path
        The file path to extract metadata from.

    Returns
    -------
    Dict[str, Any]
        Dictionary containing extracted metadata.

    Raises
    ------
    ValueError
        If the filename does not match the pattern.
    """
    regex_pattern = self.pattern_resolver.formatted_pattern.replace("%(", "(?P<").replace(")s", ">.*?)")
    matcher = re.match(regex_pattern, str(file_path))

    if (matcher):
      return matcher.groupdict()
    msg = f"Filename '{file_path}' does not match the expected pattern: {self.pattern_resolver.formatted_pattern}"
    raise ValueError(msg)

  @property
  def files(self) -> FilteredFiles:
    """Map files in the root directory to their extracted metadata.

    Returns
    -------
    FilteredFiles
        An instance of FilteredFiles containing the mapped files.
    """
    if self.mapped_files:
      return FilteredFiles(files=self.mapped_files)

    unmatched = []
    for file_path in self.locate_files():
      try:
        metadata = self.extract_metadata(file_path.relative_to(self.root_directory))
        metadata["file_path"] = file_path
        self.mapped_files.append(metadata)
      except ValueError as ve:
        unmatched.append(file_path)
        if self.show_warnings:
          logger.warning(
            f"Skipping file {file_path}, as it does not match the pattern.", 
            error=ve, 
            valid_keys=self.pattern_resolver.keys
          )
    if unmatched:
      logger.debug(f"Unmatched files: {len(unmatched)}", unmatched=unmatched)
    return FilteredFiles(files=self.mapped_files)


if __name__ == "__main__":  # pragma: no cover
  import subprocess
  import tempfile
  from pathlib import Path


  ################################################################################################
  # MAKE SOME FAKE DATA
  ################################################################################################
  temp_path = Path(tempfile.mkdtemp())
  temp_path.mkdir(parents=True, exist_ok=True)

  for i in range(1, 4):
    for k in range(1, 6):
      for feature_type in ["some", "other", "features"]:
        fp = temp_path / "example_data" / f"PatientID-{i:03d}" / f"Series-{k:02d}" / f"features-{feature_type}.txt"
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(f"Example content {i}-{k}-{feature_type}")

  tree_output = subprocess.check_output(["tree", "-F", temp_path])
  print(tree_output.decode("utf-8")) # noqa

  ################################################################################################
  # Example usage
  ################################################################################################

  from rich import print  # noqa
  # Define a filename pattern
  FILE_PATTERN = "example_data/PatientID-{PatientID}/Series-{Series}/features-{feature_type}.txt"

  # Initialize BaseReader
  reader = BaseReader(root_directory=temp_path, filename_pattern=FILE_PATTERN)

  print(
    reader
    .files
    .filter(filters=[{"PatientID": ["001", "002"]}, {"Series": ["01", "04"]}, {"feature_type": "some"}])
  )

  print(
    reader.files
    .filter(PatientID="001")
    .filter(Series=lambda x: x in ["01", "04"])
    .filter(feature_type="some")
  )
