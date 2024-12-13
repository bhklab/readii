import pytest
import SimpleITK as sitk
import numpy as np
from pathlib import Path
from readii.io.writers.nifti_writer import NIFTIWriter, NiftiWriterValidationError, NiftiWriterIOError # type: ignore

@pytest.fixture
def sample_image():
    """Fixture for creating a sample SimpleITK image."""
    image = sitk.Image(10, 10, sitk.sitkUInt8)
    return image

@pytest.fixture
def sample_array():
    """Fixture for creating a sample numpy array."""
    array = np.zeros((10, 10), dtype=np.uint8)
    return array

@pytest.fixture
def nifti_writer(tmp_path):
    """Fixture for creating a NIFTIWriter instance."""
    return NIFTIWriter(
        root_directory=tmp_path,
        filename_format="{PatientID}.nii.gz",
        compression_level=5,
        overwrite=False,
        create_dirs=True,
    )

@pytest.mark.parametrize("image", ["not_an_image", 12345])
def test_save_invalid_image(nifti_writer, image):
    """Test saving an invalid image."""
    with pytest.raises(NiftiWriterValidationError):
        nifti_writer.save(image=image, PatientID="12345")

@pytest.mark.parametrize("image", ["sample_image", "sample_array"])
def test_save_valid_image(nifti_writer, request, image):
    """Test saving a valid image."""
    image = request.getfixturevalue(image)
    out_path = nifti_writer.save(image=image, PatientID="12345")
    assert out_path.exists()

def test_save_existing_file_without_overwrite(nifti_writer, sample_image):
    """Test saving when file already exists and overwrite is False."""
    nifti_writer.save(sample_image, PatientID="12345")
    with pytest.raises(NiftiWriterIOError):
        nifti_writer.save(sample_image, PatientID="12345")

def test_save_existing_file_with_overwrite(nifti_writer, sample_image):
    """Test saving when file already exists and overwrite is True."""
    nifti_writer.overwrite = True
    nifti_writer.save(sample_image, PatientID="12345")
    assert nifti_writer.save(sample_image, PatientID="12345").exists()

@pytest.mark.parametrize("compression_level", [0, 5, 9])
def test_save_with_different_compression_levels(nifti_writer, sample_image, compression_level):
    """Test saving with different compression levels."""
    nifti_writer.compression_level = compression_level
    out_path = nifti_writer.save(sample_image, PatientID="12345")
    assert out_path.exists()

@pytest.mark.parametrize("filename_format", ["{PatientID}.nii", "{PatientID}.nii.gz"])
def test_save_with_different_filename_formats(nifti_writer, sample_image, filename_format):
    """Test saving with different filename formats."""
    nifti_writer.filename_format = filename_format
    out_path = nifti_writer.save(sample_image, PatientID="12345")
    assert out_path.exists()

@pytest.mark.parametrize("key,value", [("Modality", "T1"), ("Region", "Brain")])
def test_save_with_additional_keys(nifti_writer, sample_image, key, value):
    """Test saving with additional keys."""
    out_path = nifti_writer.save(sample_image, PatientID="12345", **{key: value})
    assert out_path.exists()
