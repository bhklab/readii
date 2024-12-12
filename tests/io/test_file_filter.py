import pytest
from pathlib import Path
from readii.io.utils import FileFilter, FilteredFiles # type: ignore

@pytest.mark.parametrize("files, filter_params, expected", [
	(
		[{"file_path": Path("file.txt"), "type": "text"}],
		{"type": "text"},
		[{"file_path": Path("file.txt"), "type": "text"}]
	),
	(
		[{"file_path": Path("file.txt"), "type": "text"}],
		{"type": "csv"},
		[]
	),
	(
		[{"file_path": Path("file_123.txt"), "id": 123}],
		{"id": 123},
		[{"file_path": Path("file_123.txt"), "id": 123}]
	),
	(
		[{"file_path": Path("file_123.txt"), "id": 123}],
		{"id": 456},
		[]
	),
	(
		[
			{"file_path": Path("file.txt"), "type": "text"},
			{"file_path": Path("file.csv"), "type": "csv"}
		],
		{"type": "text"},
		[{"file_path": Path("file.txt"), "type": "text"}]
	),
	(
		[
			{"file_path": Path("file_123.txt"), "id": 123},
			{"file_path": Path("file_456.csv"), "id": 456}
		],
		{"id": 123},
		[{"file_path": Path("file_123.txt"), "id": 123}]
	),
	(
		[
			{"file_path": Path("file.txt"), "type": "text"},
			{"file_path": Path("file_123.txt"), "type": "text", "id": 123}
		],
		{"type": "text", "id": 123},
		[{"file_path": Path("file_123.txt"), "type": "text", "id": 123}]
	),
	# More complicated tests
	(
		[
			{"file_path": Path("file1.txt"), "type": "text", "id": 1},
			{"file_path": Path("file2.csv"), "type": "csv", "id": 2},
			{"file_path": Path("file3.txt"), "type": "text", "id": 3}
		],
		{"type": "text"},
		[
			{"file_path": Path("file1.txt"), "type": "text", "id": 1},
			{"file_path": Path("file3.txt"), "type": "text", "id": 3}
		]
	),
	(
		[
			{"file_path": Path("file1.txt"), "type": "text", "id": 1},
			{"file_path": Path("file2.csv"), "type": "csv", "id": 2},
			{"file_path": Path("file3.txt"), "type": "text", "id": 3}
		],
		{"type": "text", "id": 3},
		[{"file_path": Path("file3.txt"), "type": "text", "id": 3}]
	),
	# Test filtering with multiple criteria
	(
		[
			{"file_path": Path("file1.txt"), "type": "text", "id": 1},
			{"file_path": Path("file2.csv"), "type": "csv", "id": 2},
			{"file_path": Path("file3.txt"), "type": "text", "id": 3}
		],
		{"type": "text", "id": [1, 3]},
		[
			{"file_path": Path("file1.txt"), "type": "text", "id": 1},
			{"file_path": Path("file3.txt"), "type": "text", "id": 3}
		]
	),
	# Test filtering with a list of values
	(
		[
			{"file_path": Path("file1.txt"), "type": "text"},
			{"file_path": Path("file2.csv"), "type": "csv"},
			{"file_path": Path("file3.txt"), "type": "text"}
		],
		{"type": ["text", "csv"]},
		[
			{"file_path": Path("file1.txt"), "type": "text"},
			{"file_path": Path("file2.csv"), "type": "csv"},
			{"file_path": Path("file3.txt"), "type": "text"}
		]
	),
	# Test filtering with missing keys
	(
		[
			{"file_path": Path("file1.txt"), "type": "text"},
			{"file_path": Path("file2.csv")},
			{"file_path": Path("file3.txt"), "type": "text"}
		],
		{"type": "text"},
		[
			{"file_path": Path("file1.txt"), "type": "text"},
			{"file_path": Path("file3.txt"), "type": "text"}
		]
	),
	# Test filtering with no matching criteria
	(
		[
			{"file_path": Path("file1.txt"), "type": "text"},
			{"file_path": Path("file2.csv"), "type": "csv"}
		],
		{"type": "image"},
		[]
	),
	# Test filtering with empty files list
	(
		[],
		{"type": "text"},
		[]
	),
	# Test filtering with callable criteria
	(
		[
			{"file_path": Path("file1.txt"), "type": "text", "size": 100},
			{"file_path": Path("file2.csv"), "type": "csv", "size": 200},
			{"file_path": Path("file3.txt"), "type": "text", "size": 300}
		],
		{"size": lambda x: x > 150},
		[
			{"file_path": Path("file2.csv"), "type": "csv", "size": 200},
			{"file_path": Path("file3.txt"), "type": "text", "size": 300}
		]
	),
	# Test filtering with missing keys and callable criteria
	(
		[
			{"file_path": Path("file1.txt"), "type": "text"},
			{"file_path": Path("file2.csv")},
			{"file_path": Path("file3.txt"), "type": "text", "size": 300}
		],
		{"size": lambda x: x is not None and x > 150},
		[
			{"file_path": Path("file3.txt"), "type": "text", "size": 300}
		]
	),
])
def test_filter(files, filter_params, expected):
	result = FileFilter.filter(files, **filter_params)
	assert result == expected

def test_filtered_files():
	files = [
		{"file_path": Path("file1.txt"), "type": "text", "id": 1},
		{"file_path": Path("file2.csv"), "type": "csv", "id": 2},
		{"file_path": Path("file3.txt"), "type": "text", "id": 3}
	]
	filtered_files = FilteredFiles(files)
	assert len(filtered_files) == 3

	filtered = filtered_files.filter(type="text")
	assert len(filtered) == 2
	assert filtered.files == [
		{"file_path": Path("file1.txt"), "type": "text", "id": 1},
		{"file_path": Path("file3.txt"), "type": "text", "id": 3}
	]

	filtered = filtered_files.filter(type="text", id=3)
	assert len(filtered) == 1
	assert filtered.files == [
		{"file_path": Path("file3.txt"), "type": "text", "id": 3}
	]

	filtered = filtered_files.filter(type="image")
	assert len(filtered) == 0

def test_filtered_files_iteration():
	files = [
		{"file_path": Path("file1.txt"), "type": "text", "id": 1},
		{"file_path": Path("file2.csv"), "type": "csv", "id": 2},
		{"file_path": Path("file3.txt"), "type": "text", "id": 3}
	]
	filtered_files = FilteredFiles(files)
	iter_files = list(iter(filtered_files))
	assert iter_files == files
