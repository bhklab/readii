from pathlib import Path

import SimpleITK as sitk

from readii.io.writers.base_writer import BaseWriter
from readii.utils import logger


class NIFTIWriter(BaseWriter):
    """Class for managing file writing with customizable paths and filenames for NIFTI files."""

    def save(self, image: sitk.Image, SubjectID: str, **kwargs: str | int) -> Path:
        """Write the given data to the file resolved by the given kwargs."""
        out_path = self.resolve_path(SubjectID=SubjectID, **kwargs)
        logger.debug("Writing image to file", out_path=out_path)
        sitk.WriteImage(image, str(out_path), useCompression=True, compressionLevel=9)
        return out_path


if __name__ == "__main__":  # noqa
    from pathlib import Path  # noqa

    # Example usage
    nifti_writer = NIFTIWriter(
        root_directory=Path("TRASH", "negative_controls"),
        filename_format="{NegativeControl}_{Region}/{date}-{SubjectID}_{Modality}.nii.gz",
    )

    # This would create a directory structure like:
    # TRASH/
    #     negative_controls/
    #       Randomized_ROI/
    #         2022-01-01-JohnAdams_CT.nii.gz
    #       Sampled_NonROI/
    #         2022-01-01-JohnAdams_CT.nii.gz
    # note: this file structure is probably confusing, but just showing how the file names are generated

    # The keyword arguments passed here MUST match the placeholders in the filename format
    nifti_writer.save(
        image=sitk.Image(10, 10, 10, sitk.sitkInt16),
        SubjectID="JohnAdams",
        NegativeControl="Randomized",
        Region="Brain",
        Modality="CT",
        # note, the date and time are generated automatically!
    )
