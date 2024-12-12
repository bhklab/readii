import pytest
from pathlib import Path
from readii.io.utils import DirectoryScanner, DirectoryScannerError # type: ignore

@pytest.mark.parametrize("root_directory, expected_exception", [
  (Path("/non/existent/path"), DirectoryScannerError),
  (Path(__file__), DirectoryScannerError),
  (Path("."), None),
])
def test_scan(root_directory, expected_exception):
  scanner = DirectoryScanner(root_directory)
  if expected_exception:
    with pytest.raises(expected_exception):
      scanner.scan()
  else:
    result = scanner.scan()
    assert isinstance(result, list)

@pytest.mark.parametrize("include_files, include_directories, expected_count", [
  (True, False, 2),
  (False, True, 1),
  (True, True, 3),
])
def test_scan_include_files_and_directories(tmp_path, include_files, include_directories, expected_count):
  (tmp_path / "file1.txt").touch()
  (tmp_path / "file2.txt").touch()
  (tmp_path / "dir").mkdir()
  scanner = DirectoryScanner(tmp_path, include_files=include_files, include_directories=include_directories)
  result = scanner.scan()
  assert len(result) == expected_count

@pytest.mark.parametrize("glob_pattern, expected_count, expected_names", [
  ("*.txt", 1, ["file1.txt"]),
  ("*.log", 1, ["file2.log"]),
  ("*", 2, ["file1.txt", "file2.log"]),
])
def test_scan_glob_pattern(tmp_path, glob_pattern, expected_count, expected_names):
  (tmp_path / "file1.txt").touch()
  (tmp_path / "file2.log").touch()
  scanner = DirectoryScanner(tmp_path, glob_pattern=glob_pattern)
  result = scanner.scan()
  assert len(result) == expected_count
  assert sorted([p.name for p in result]) == sorted(expected_names)

@pytest.mark.parametrize("recursive, expected_count", [
  (True, 2),
  (False, 1),
])
def test_scan_recursive(tmp_path, recursive, expected_count):
  (tmp_path / "file1.txt").touch()
  (tmp_path / "subdir").mkdir()
  (tmp_path / "subdir" / "file2.txt").touch()
  scanner = DirectoryScanner(tmp_path, recursive=recursive)
  result = scanner.scan()
  assert len(result) == expected_count
