from importlib import resources

def get_NSCLC_SEG():
    """ Get path to example NSCLC Radiogenomics R01-001 SEG [1] file path.

    Returns
    -------
    pathlib.PosixPath
        Path to directory.
    
    References
    ----------
    https://wiki.cancerimagingarchive.net/display/Public/NSCLC+Radiogenomics
    """
    with resources.path("yarea.data", "1-1.dcm") as f:
        data_file_path = f
    
    return data_file_path
