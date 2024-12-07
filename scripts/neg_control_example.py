from dataclasses import asdict, dataclass
from logging import getLogger
from pathlib import Path
from typing import Dict, List, Pattern

import click
import yaml
from imgtools.autopipeline import (
	ImageAutoInput,
)
from imgtools.cli import set_log_verbosity
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from readii import loaders as rdloaders
from readii.io import NIFTIWriter
from readii.negative_controls_refactor import NegativeControlManager
from readii.utils import logger

logger.setLevel("INFO")
logger.debug("Starting Notebook.")

# setting imgtools logging to ERROR to avoid spamming the console
imgtools_logger = getLogger("imgtools")
imgtools_logger.setLevel("ERROR")

@dataclass
class Config:
	"""Configuration class for radiomics pipeline.

	Attributes
	----------
		INPUT_DATA: Path to input data directory
		OUTPUT_DATA: Path to output data directory
		MODALITIES: String specifying imaging modalities to process
		NEGATIVE_CONTROLS: List of negative control types
		NEGATIVE_CONTROL_REGIONS: List of regions to use as negative controls
		RANDOM_SEED: Integer seed for random number generation
		ROI_OF_INTEREST: Dictionary mapping region names to regex patterns
	"""

	INPUT_DATA: Path
	OUTPUT_DATA: Path
	MODALITIES: str
	NEGATIVE_CONTROLS: List[str]
	NEGATIVE_CONTROL_REGIONS: List[str]
	RANDOM_SEED: int
	ROI_OF_INTEREST: Dict[str, Pattern]

	@classmethod
	def from_dict(cls, config_dict: dict) -> "Config":
		"""Create Config instance from dictionary.

		Parameters
		----------
			config_dict: Dictionary containing configuration parameters

		Returns
		-------
			Config instance initialized with provided parameters
		"""
		config_dict["INPUT_DATA"] = Path(config_dict["INPUT_DATA"])
		config_dict["OUTPUT_DATA"] = Path(config_dict["OUTPUT_DATA"])
		
		return cls(**config_dict)


def run(config: dict) -> None:
	"""Run the pipeline."""
	###############################################################################
	# Med-ImageTools Run
	###############################################################################

	dataset = ImageAutoInput(
		dir_path=config.INPUT_DATA.absolute(),
		modalities=config.MODALITIES,
		update=True,
		n_jobs=-1,
		visualize=False,
	)

	###############################################################
	# Create a NegativeControlManager object
	ncm = NegativeControlManager.from_strings(
		negative_control_types=config.NEGATIVE_CONTROLS,
		region_types=config.NEGATIVE_CONTROL_REGIONS,
		random_seed=config.RANDOM_SEED,
	)

	###############################################################
	# Two writers, one for the original images and one for the negative controls
	neg_nifti_writer = NIFTIWriter(
		root_directory=config.OUTPUT_DATA,
		filename_format="{SubjectID}/{Modality}/{Filename}.nii.gz",
	)

	###############################################################

	dataset_df = dataset.df_combined
	ct_loader = rdloaders.loadDicomSITK
	rt_loader = rdloaders.loadRTSTRUCTSITK

	# Pseudocode
	# -------
	# for loop 1:
	#   for each row (patient) in dataset_df (output of MediaImageTools Crawler + Edges):
	#     load CT and RTSTRUCT
	#     for each ROI in the RTSTRUCT:
	#       load the mask for that ROI
	#       for each negative control strategy & region strategy:
	#         apply the negative control strategy to the region strategy
	#         save the output to the negative control output directory
	#
	# damn 3 nested for loops (not serious if only one ROI, but should allow users to use multiple ROIs)

	# iterate over the rows of the dataframe
	with logging_redirect_tqdm(
		[getLogger("readii"), getLogger("imgtools")]
	):  # weird way to get the logs to not mess up tqdm
		pbar_subjects = tqdm(dataset_df.itertuples(), total=len(dataset_df), leave=False)
		for row in pbar_subjects:
			logger.info(f"Processing Patient: {row.patient_ID}")
			pbar_subjects.set_description(f"Processing Patient: {row.patient_ID:>20}")
			ct_path = Path(row.folder_CT)
			mask_path = Path(row.folder_RTSTRUCT_CT)

			logger.info("Loading CT", ct_path=ct_path)
			base_image = ct_loader(ct_path)

			logger.info("Loading RTSTRUCT", mask_path=mask_path)
			masks = rt_loader(
				rtstructPath=mask_path, baseImageDirPath=ct_path, roiNames=config.ROI_OF_INTEREST
			)

			logger.info("Writing original CT image")
			# write the original images again
			neg_nifti_writer.save(
				SubjectID=row.patient_ID,
				image=base_image,
				Modality="CT",
				Filename="original",
			)

			# for roi, mask_image in masks.items():
			pbar_ROIs = tqdm(
				masks.items(),
				total=len(masks),
				leave=False,
			)
			for roi, mask_image in pbar_ROIs:
				logger.info(f"Processing ROI: {roi}")
				pbar_ROIs.set_description(f"Processing ROIname: {roi:>20}")
				logger.info("Writing original RTSTRUCT image")
				neg_nifti_writer.save(
					SubjectID=row.patient_ID,
					image=mask_image,
					Modality="RTSTRUCT",
					Filename=roi,
				)


				pbar_negctrls = tqdm(
					ncm.strategy_products,
					total=len(ncm),
					leave=False,
				)
				for nc, st in pbar_negctrls:
					# logger.info(f"Processing negative control: {nc.name()} & {st.name()}")
					desc = f"{nc.name()} + {st.name()}"
					pbar_negctrls.set_description(f"Processing Negctrl: {desc:>20}")
					nc_image, nc_name, region_name = ncm.apply_single(
						base_image, mask_image, nc, st
					)

					# could return this as a dict and then save it to the writer
					logger.info("Writing negative control image", nc_name=nc_name, region_name=region_name)
					_ = neg_nifti_writer.save(
						SubjectID=row.patient_ID,
						image=nc_image,
						Modality="CT",
						Filename=f"{roi}/{nc_name}-{region_name}",
					)

# @set_log_verbosity(logger_name="readii")
@click.command()
@click.option(
	"--config",
	"-c",
	type=click.Path(exists=True, path_type=Path),
	default="readii_run.yaml",
	help="Path to the configuration file.",
)
def main(config: Path, verbose: int = 0, quiet: bool = False) -> None:
	"""Run the pipeline."""
	config_dict = yaml.safe_load(config.open("r"))
	config = Config.from_dict(config_dict)
	logger.debug("Running with config:", config=asdict(config))
	run(config)


if __name__ == "__main__":
	main()
