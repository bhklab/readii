# wrap this around MedImage?

import multiprocessing
from pathlib import Path 
import SimpleITK as sitk
import numpy as np

from pydantic import (
    BaseModel,
    Field,
)


class ScanInput(BaseModel):
    """
    Configuration model for processing medical scan samples.

    This class provides a standardized configuration for loading and processing
    medical scans (CT, MR, PT).
    """

    filepath: Path = Field(
        description="Path to the medical scan image file to load. Absolute path or relative to the current working directory.",
        title="Scan Filepath",
        examples=[
            "data/NSCLC-Radiomics/images/mit_NSCLC-Radiomics/LUNG1-001_0000/CT_63382046/CT.nii.gz", 
            "/absolute/path/to/image/data/file/MR.nii.gz"],
    )
    index_file: Path = Field(
        description="Path to an index CSV file with metadata for the images, including reference info for segmentation masks and scan.",
        title="Index File",
        examples=["data/NSCLC-Radiomics/mit_NSCLC-Radiomics_index-simple.csv", "/absolute/path/to/metadata/image_index.csv"]
    )
    dataset_name: str | None = Field(
        default=None,
        description="Name of the dataset, defaults to input directory base name if not provided. Used for organizing outputs and labeling results.",
        title="Dataset Name",
        min_length=1,
        max_length=100,
        examples=["NSCLC-Radiomics", "Head-Neck-PET-CT"],
    )
    @classmethod
    def build(
        cls,
        filepath: str | Path,
        

    ):
        return
    @classmethod
    def flatten(
        cls,
        image: sitk.Image
    ) -> sitk.Image:
        """Remove axes of image with size one. (ex. shape is [1, 100, 256, 256]).

        Parameters
        ----------
        image : sitk.Image
            Image to remove axes with size one.

        Returns
        -------
        sitk.Image
            image with axes of length one removed.
        """
        imageArr = sitk.GetArrayFromImage(image)

        imageArr = np.squeeze(imageArr)

        return sitk.GetImageFromArray(imageArr)

    # n_jobs: int = Field(
    #     default=max(1, multiprocessing.cpu_count() - 2),
    #     description="Number of parallel jobs to run for negative control generation. Default reserves 2 cores for system operations.",
    #     title="Parallel Jobs",
    #     ge=1,  # Greater than or equal to 1
    #     le=multiprocessing.cpu_count(),  # Less than or equal to available cores
    #     examples=[4, 8, 12],
    # )
    # regions: list[str] | None = Field(
    #     default=None,
    #     description="Regions to use in negative control generation. None means include all regions.",
    #     title="Region Strategies",
    #     examples=[
    #         ["Full", "ROI"],
    #         ["Background", "ROI"]
    #     ]
    # )
    # permutations: list[str] | None = Field(
    #     default=None,
    #     description="Permutations to use in negative control generation. None means include all permutations.",
    #     title="Permutation Strategies",
    #     examples=[
    #         ["Random"],
    #         ["Sample", "Shuffle"]
    #     ]
    # )
    # crop: str | None = Field(
    #     default=None,
    #     description="Cropping method to apply to images. None means no crop will be applied.",
    #     title="Crop Method",
    #     examples=["bounding_box", "centroid", "cube"]
    # )
    # resize: int | list[int] | None = Field(
    #     default=None,
    #     description="Dimension to resize image to. If a single value, will be used for all image dimensions. If list, must match image dimension.",
    #     title="Resize Dimension",
    #     examples=[50, [256, 256, 50]]
    # )
    