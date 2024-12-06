#d %%
from logging import getLogger
from pathlib import Path

import pandas as pd
import SimpleITK as sitk
import yaml
from imgtools.autopipeline import AutoPipeline
from rich import print  # noqa
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from readii.io import NIFTIWriter
from readii.negative_controls_refactor import NegativeControlManager
from readii.utils import logger

logger.setLevel("INFO")
logger.debug("Starting Notebook.")

# %%
data_dir = Path().cwd() / "TRASH" / "data"
INPUT_DATA = data_dir / "dicom"

# idk save med-imagetools to temp dir 
OUTPUT_DATA = Path('/tmp') / "mit-generated-niftis"
NEGATIVE_CONTROL_OUTPUT_DIR = data_dir / "negative-controls-niftis" 

# These could probably be in a config file
MODALITIES = "CT,RTSTRUCT"
CT_FILE_NAME = "CT.nii.gz"
ROI_OF_INTEREST = "GTV"
RTSTRUCT_FILE_NAME = f"{ROI_OF_INTEREST}.nii.gz"  # Not used to CREATE, but used to MATCH against med-imagetools

NEGATIVE_CONTROLS = ["sampled", "shuffled", "randomized"]
NEGATIVE_CONTROL_REGIONS = ["roi", "non_roi", "full"]
RANDOM_SEED = 10

# %% [markdown]
# # Initialize 

# %%
# Make sure the directories exist 
OUTPUT_DATA.mkdir(exist_ok=True)

# delete NEGATIVE_CONTROL_OUTPUT_DIR 
if NEGATIVE_CONTROL_OUTPUT_DIR.exists():
  import shutil
  shutil.rmtree(NEGATIVE_CONTROL_OUTPUT_DIR)

# Save the ROI regex to a YAML file
roi_matches = {
  ROI_OF_INTEREST: "^(GTV1)$"
}

with Path(INPUT_DATA, "mit_roi_names.yaml").open("w") as outfile:
    yaml.dump(roi_matches, outfile)

# %% [markdown]
# # Med-ImageTools Run

# %%
# pipeline = AutoPipeline(input_directory=INPUT_DATA,
#                         output_directory=OUTPUT_DATA,
#                         modalities=MODALITIES,
#                         spacing=(0., 0., 0.),
#                         ignore_missing_regex = True,
#                         update=True,
#                         read_yaml_label_names = True,
#                         roi_yaml_path = Path(INPUT_DATA, "mit_roi_names.yaml")
#                         )

# pipeline.run()

# %% [markdown]
# # Negative Control Builder

# %%
###############################################################
# Create a NegativeControlManager object
ncm = NegativeControlManager.from_strings(
  negative_control_types=NEGATIVE_CONTROLS,
  region_types=NEGATIVE_CONTROL_REGIONS,
  random_seed=RANDOM_SEED,
)


###############################################################
# Two writers, one for the original images and one for the negative controls
original_nifti_writer = NIFTIWriter(
  root_directory=NEGATIVE_CONTROL_OUTPUT_DIR,
  filename_format="{SubjectID}/{Modality}/original.nii.gz",
)

neg_nifti_writer = NIFTIWriter(
  root_directory=NEGATIVE_CONTROL_OUTPUT_DIR,
  filename_format="{SubjectID}/{Modality}/{NegativeControl}-{Region}.nii.gz",
)


###############################################################

images_metadata = pd.read_csv(
  OUTPUT_DATA / "dataset.csv",
  index_col=0,
)

# iterate over the rows of the dataframe
# iterate over the rows of the dataframe
readii_logger = getLogger('readii')
with logging_redirect_tqdm([readii_logger]):
	for row in tqdm(
		images_metadata.itertuples(), total=len(images_metadata), desc="Processing subjects"
	):
		ct_path = OUTPUT_DATA / row.output_folder_CT / CT_FILE_NAME
		mask_path = OUTPUT_DATA / row.output_folder_RTSTRUCT_CT / RTSTRUCT_FILE_NAME
		logger.info(f"Processing row: {row.Index}")
		base_image = sitk.ReadImage(ct_path)
		mask_image = sitk.ReadImage(mask_path)

		# write the original images again
		original_nifti_writer.save(
			SubjectID=row.Index,
			image=base_image,
			Modality="CT",
		)

		original_nifti_writer.save(
			SubjectID=row.Index,
			image=mask_image,
			Modality="RTSTRUCT",
		)
		for nc, st in tqdm(
			ncm.strategy_products,
			total=len(ncm),
			desc="Processing negctrls",
			leave=False,
		):
			logger.info(f"Processing negative control: {nc.name()} & {st.name()}")
			image, nc_name, region_name = ncm.apply_single(base_image, mask_image, nc, st)
			output_nifti_path = neg_nifti_writer.save(
				SubjectID=row.Index,
				image=image,
				NegativeControl=nc_name,
				Region=region_name,
				Modality="CT",
			)

# %%
from readii.io.readers import NIFTIReader

original_nifti_reader = NIFTIReader(
			# root_directory=Path("TRASH/data/nifti"),
			root_directory=NEGATIVE_CONTROL_OUTPUT_DIR,
			filename_pattern="{SubjectID}/{Modality}/original.nii.gz",
)

neg_nifti_reader = NIFTIReader(
			# root_directory=Path("TRASH/data/negative-controls-niftis"),
			root_directory=NEGATIVE_CONTROL_OUTPUT_DIR,
			filename_pattern="{SubjectID}/{Modality}/{NegativeControl}-{Region}.nii.gz",
	)

original = original_nifti_reader.map_files()
results = neg_nifti_reader.map_files()

print(original)
print(results)


# %%



