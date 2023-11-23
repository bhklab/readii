from area_bk.loaders import *

def test_loadDicomSITK():
    """Test loading DICOM from directory."""
    actual = loadDicomSITK("tests/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741")
    assert type(actual) == sitk.Image