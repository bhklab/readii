
import os
import pytest
from pathlib import Path
from readii.io.writers.base_writer import BaseWriter

class SimpleWriter(BaseWriter):
    def save(self, content: str) -> Path:
        file_path = self.resolve_path()
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

class MediumWriter(BaseWriter):
    def save(self, content: str, suffix: str = '') -> Path:
        file_path = self.resolve_path(suffix=suffix)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

class ComplexWriter(BaseWriter):
    def save(self, content: str, metadata: dict) -> Path:
        file_path = self.resolve_path(**metadata)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

def test_simple_writer(temp_dir):
    writer = SimpleWriter(root_directory=temp_dir, filename_format="{date_time}.txt")
    with writer:
        file_path = writer.save("Simple content")
    assert file_path.exists()
    assert file_path.read_text() == "Simple content"

def test_medium_writer(temp_dir):
    writer = MediumWriter(root_directory=temp_dir, filename_format="{date_time}_{suffix}.txt")
    with writer:
        file_path = writer.save("Medium content", suffix="test")
    assert file_path.exists()
    assert file_path.read_text() == "Medium content"

def test_complex_writer(temp_dir):
    writer = ComplexWriter(root_directory=temp_dir, filename_format="{date_time}_{user}.txt")
    with writer:
        file_path = writer.save("Complex content", metadata={"user": "testuser"})
    assert file_path.exists()
    assert file_path.read_text() == "Complex content"

def test_context_manager_cleanup(temp_dir):
    subdir = temp_dir / "nested"
    writer = SimpleWriter(root_directory=subdir, filename_format="{date_time}.txt")
    with writer:
        assert subdir.exists()
    assert not subdir.exists()

def test_directory_creation(temp_dir):
    writer = SimpleWriter(root_directory=temp_dir / "nested", filename_format="{date_time}.txt")
    with writer:
        file_path = writer.save("Content")
    assert file_path.exists()
    assert file_path.read_text() == "Content"
    assert (temp_dir / "nested").exists()

def test_directory_not_created_if_exists(temp_dir):
    existing_dir = temp_dir / "existing"
    existing_dir.mkdir()
    writer = SimpleWriter(root_directory=existing_dir, filename_format="{date_time}.txt")
    with writer:
        file_path = writer.save("Content")
    assert file_path.exists()
    assert file_path.read_text() == "Content"
    assert existing_dir.exists()

def test_no_create_dirs_non_existent(temp_dir):
    with pytest.raises(FileNotFoundError):
        with SimpleWriter(root_directory=temp_dir / "nested_non_existent", filename_format="{date_time}.txt", create_dirs=False) as writer:
            file_path = writer.save("Content")
