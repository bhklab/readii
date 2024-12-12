import os
import pytest
from pathlib import Path
from typing import Any
from readii.io.utils.base_reader import BaseReader # type: ignore

class CSVReader(BaseReader):
    def __init__(self, root_directory: str | Path, **scanner_kwargs: Any) -> None:
        super().__init__(root_directory, filename_pattern="data/PatientID-{PatientID}/csv/Series-{Series}.csv", **scanner_kwargs)

class JSONReader(BaseReader):
    def __init__(self, root_directory: str | Path, **scanner_kwargs: Any) -> None:
        super().__init__(root_directory, filename_pattern="data/PatientID-{PatientID}/json/Series-{Series}.json", **scanner_kwargs)

@pytest.fixture
def temp_dir(tmp_path):
    # Create a temporary directory with some test files
    for i in range(1, 4):
        for k in range(1, 6):
            csv_fp = tmp_path / "data" / f"PatientID-{i:03d}" / "csv" / f"Series-{k:02d}.csv"
            json_fp = tmp_path / "data" / f"PatientID-{i:03d}" / "json" / f"Series-{k:02d}.json"
            csv_fp.parent.mkdir(parents=True, exist_ok=True)
            json_fp.parent.mkdir(parents=True, exist_ok=True)
            csv_fp.write_text(f"CSV content {i}-{k}")
            json_fp.write_text(f"JSON content {i}-{k}")
    return tmp_path

def test_locate_csv_files(temp_dir):
    reader = CSVReader(root_directory=temp_dir)
    files = reader.files
    assert len(files) == 15  # 3 patients * 5 series

def test_locate_json_files(temp_dir):
    reader = JSONReader(root_directory=temp_dir)
    files = reader.files
    assert len(files) == 15  # 3 patients * 5 series

def test_extract_csv_metadata(temp_dir):
    reader = CSVReader(root_directory=temp_dir)
    file_path = temp_dir / "data" / "PatientID-001" / "csv" / "Series-01.csv"
    metadata = reader.extract_metadata(file_path.relative_to(temp_dir))
    assert metadata == {"PatientID": "001", "Series": "01"}

def test_extract_json_metadata(temp_dir):
    reader = JSONReader(root_directory=temp_dir)
    file_path = temp_dir / "data" / "PatientID-001" / "json" / "Series-01.json"
    metadata = reader.extract_metadata(file_path.relative_to(temp_dir))
    assert metadata == {"PatientID": "001", "Series": "01"}

def test_csv_files_property(temp_dir):
    reader = CSVReader(root_directory=temp_dir)
    files = reader.files
    assert len(files.files) == 15  # 3 patients * 5 series

def test_json_files_property(temp_dir):
    reader = JSONReader(root_directory=temp_dir)
    files = reader.files
    assert len(files.files) == 15  # 3 patients * 5 series

def test_csv_files_filtering(temp_dir):
    reader = CSVReader(root_directory=temp_dir)
    filtered_files = reader.files.filter(filters=[{"PatientID": ["001", "002"]}, {"Series": ["01", "04"]}])
    assert len(filtered_files.files) == 4  # 2 patients * 2 series

def test_json_files_filtering(temp_dir):
    reader = JSONReader(root_directory=temp_dir)
    filtered_files = reader.files.filter(filters=[{"PatientID": ["001", "002"]}, {"Series": ["01", "04"]}])
    assert len(filtered_files.files) == 4  # 2 patients * 2 series

def test_invalid_csv_pattern(temp_dir):
    reader = CSVReader(root_directory=temp_dir)
    with pytest.raises(ValueError):
        reader.extract_metadata(Path("invalid_pattern/PatientID-001/csv/Series-01.csv"))

def test_invalid_json_pattern(temp_dir):
    reader = JSONReader(root_directory=temp_dir)
    with pytest.raises(ValueError):
        reader.extract_metadata(Path("invalid_pattern/PatientID-001/json/Series-01.json"))

def test_no_matching_csv_files(temp_dir):
    reader = CSVReader(root_directory=temp_dir)
    reader.pattern_resolver.formatted_pattern = "non_matching_pattern"
    files = reader.files
    assert len(files.files) == 0

def test_no_matching_json_files(temp_dir):
    reader = JSONReader(root_directory=temp_dir)
    reader.pattern_resolver.formatted_pattern = "non_matching_pattern"
    files = reader.files
    assert len(files.files) == 0
