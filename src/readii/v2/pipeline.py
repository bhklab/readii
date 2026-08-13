from pathlib import Path
import multiprocessing
from readii.v2.scan_input import SampleInput
from readii.negative_controls_refactor import NegativeControlManager, ImageInput
from imgtools.io.sample_output import ExistingFileMode
from imgtools.io.writers.nifti_writer import NIFTIWriter, NiftiWriterIOError
import pandas as pd
from imgtools.coretypes import MedImage, Mask
from typing import TYPE_CHECKING, Any

# def process_one_sample(
#     args: tuple[
#         str,
#         Path,
#         Path,
#         SampleInput,
#         NegativeControlManager, 
#     ]
# ):
#     """
#     Process a single medical imaging sample through the complete pipeline.

#     The single 'args' tuple contains the following elements, likely passed in
#     from the components of the autopipeline class:
#     - idx: str (arbitrary, generated from enumerate)
#     - scan_path: Path (path to the )
#     """
#     return


# class Pipeline:
#     """Pipeline for negative control generation."""

#     input: SampleInput
#     nc_manager: NegativeControlManager


def process_one(
    image_dir: str | Path,
    scan_metadata: pd.Series | dict[str, Any],
    mask_metadata: pd.Series | dict[str, Any],
    nc_manager: NegativeControlManager,
    scan_writer: NIFTIWriter,
    mask_writer: NIFTIWriter | None = None
    ):
    """
    
    Parameters
    ----------
    image_dir : str | Path
        Path to the root image directory that the scan and mask image paths work off of
    scan_metadata : pd.Series | dict[str, Any]
        Metadata for scan (like from med-imagetools index-simple.csv file). Must include filepath.
    mask_metadata
        Metadata for mask referencing scan (like from med-imagetools index-simple.csv file). Must include filepath.
    nc_manager
        Negative control manager to use on the images
    
    """
    scan_metadata = scan_metadata.to_dict() if isinstance(scan_metadata, pd.Series) else scan_metadata
    mask_metadata = mask_metadata.to_dict() if isinstance(mask_metadata, pd.Series) else mask_metadata

    # want output to be dataset/images/readii/control_name/sample_id/CT_#######/CT.nii.gz
    # {region}_{permutation}_{crop}_{resize}
    scan = MedImage.from_file(
        filepath = scan_metadata['filepath'],
        metadata = scan_metadata
    )
    mask = Mask.from_file(
        filepath = mask_metadata[mask_metadata],
        metadata = mask_metadata
    )

    for proc_scan, permutation, region in nc_manager.apply(scan, mask):
        # Here would be the crop/resize 



        out_path = scan_writer.save(
            data = proc_scan,
        )
    

    return



def pipeline(
    dataset: str,
    index_file: Path,
    images_dir_path: Path = None,
    regions:list[str] | None = None, 
    permutations:list[str] | None = None, 
    crop:str | None = None, 
    resize:list[int] | None = None,
    existing_file_mode:ExistingFileMode = ExistingFileMode.FAIL,
    n_jobs: int = max(1, multiprocessing.cpu_count() - 2),
    random_seed: int = 10
):
    """Create negative control images for dataset and save them out as niftis

    """

    # want output to be dataset/images/readii/control_name/sample_id/CT_#######/CT.nii.gz


    return 


if __name__ == "__main__":
    pipeline()