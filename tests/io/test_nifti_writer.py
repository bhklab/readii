import pytest
import SimpleITK as sitk
from pathlib import Path
from readii.io.writers.nifti_writer import NIFTIWriter, NiftiWriterValidationError, NiftiWriterIOError # type: ignore

@pytest.fixture
def sample_image():
    """Fixture for creating a sample SimpleITK image."""
    image = sitk.Image(10, 10, sitk.sitkUInt8)
    return image

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

def test_invalid_compression_level():
    """Test for invalid compression level."""
    with pytest.raises(NiftiWriterValidationError):
        NIFTIWriter(
            root_directory=Path("TRASH"),
            filename_format="{PatientID}.nii.gz",
            compression_level=10,  # Invalid compression level
            overwrite=False,
            create_dirs=True,
        )

def test_invalid_filename_format():
    """Test for invalid filename format."""
    with pytest.raises(NiftiWriterValidationError):
        NIFTIWriter(
            root_directory=Path("TRASH"),
            filename_format="{PatientID}.invalid_ext",  # Invalid extension
            compression_level=5,
            overwrite=False,
            create_dirs=True,
        )

def test_save_invalid_image(nifti_writer):
    """Test saving an invalid image."""
    with pytest.raises(NiftiWriterValidationError):
        nifti_writer.save(image="not_an_image", PatientID="12345")

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
