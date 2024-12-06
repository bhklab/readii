# %%
from logging import getLogger
from pathlib import Path

import numpy as np
import pandas as pd
import SimpleITK as sitk
import yaml
from imgtools.autopipeline import (
    AutoPipeline,
    ImageAutoInput,
    ImageAutoOutput,
    Resample,
    Segmentation,
    StructureSetToSegmentation,
)
from rich import print  # noqa
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from readii.io import NIFTIWriter
from readii.negative_controls_refactor import NegativeControlManager
from readii.utils import logger

logger.setLevel("INFO")
logger.debug("Starting Notebook.")



# %%
###############################################################################
# SETUP AND CONFIGURATION
###############################################################################
_data_dir = Path().cwd() / "TRASH" / "data"
if not _data_dir.exists():
  data_dir = Path().cwd().parent / "TRASH" / "data"
  if not data_dir.exists():
    raise FileNotFoundError("Data directory not found.")
  else:
    logger.info("Using data directory from parent directory.")
else:
  data_dir = _data_dir

INPUT_DATA = data_dir / "dicom"

# idk save med-imagetools to temp dir 
# OUTPUT_DATA = Path('/tmp') / "mit-generated-niftis"
OUTPUT_DATA = data_dir / "mit-generated-niftis"
NEGATIVE_CONTROL_OUTPUT_DIR = data_dir / "negative-controls-niftis" 

# These could probably be in a config file
MODALITIES = "CT,RTSTRUCT"
SPACING=(0., 0., 0.)
CT_FILE_NAME = "CT.nii.gz"
ROI_OF_INTEREST = "GTV"
RTSTRUCT_FILE_NAME = f"{ROI_OF_INTEREST}.nii.gz"  # Not used to CREATE, but used to MATCH against med-imagetools

NEGATIVE_CONTROLS = ["sampled", "shuffled", "randomized"]
NEGATIVE_CONTROL_REGIONS = ["roi", "non_roi", "full"]
RANDOM_SEED = 10
IGNORE_MISSING_REGEX = True

# Select the first matching ROI/regex for each OAR, no duplicate matches.
ROI_SELECT_FIRST = False

# Process each matching ROI/regex as individual masks, instead of consolidating into one mask
ROI_SEPARATE = False

# Save the ROI regex to a YAML file
roi_matches = {
  ROI_OF_INTEREST: "^(GTV1)$"
}

with Path(INPUT_DATA, "mit_roi_names.yaml").open("w") as outfile:
    yaml.dump(roi_matches, outfile)


# %%
###############################################################################
# Med-ImageTools Run
###############################################################################

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
image_input = ImageAutoInput(
  dir_path = INPUT_DATA,
  modalities = MODALITIES,
  update=True,
)

# %%a

resampler = Resample(spacing=SPACING)
make_binary_mask = StructureSetToSegmentation(roi_names= roi_matches, continuous=False)


# %%

output_streams = image_input.output_streams
output = ImageAutoOutput(
  OUTPUT_DATA, 
  output_streams=output_streams, 
)
output_df_path = Path(OUTPUT_DATA, "dataset.csv")

subject_ids = image_input._loader.keys()
subject_id = subject_ids[0]

read_results = image_input(subject_id)

# %% 
for i, colname in enumerate(output_streams):  # sorted(self.output_streams)):  # CT comes before MR before PT before RTDOSE before RTSTRUCT
  modality = colname.split("_")[0]
  output_stream = ("_").join([item for item in colname.split("_") if not item.isnumeric()])
  existing_roi_indices = {"background": 0}
  match modality:
    case "CT":
      logger.info(f"Processing CT: {subject_id}")
      image = read_results[i].image
      image = resampler(image) # Note: Med-Imagetools just ignores if this errors... 

      output(subject_id, image, output_stream)
    case "RTSTRUCT":
      logger.info(f"Processing RTSTRUCT: {subject_id}")
      rtstruct = read_results[i]

      mask = make_binary_mask(
        structure_set=rtstruct,
        reference_image=image, # this is so dumb that it uses the image from the previous for loop ... lmao 
        existing_roi_indices=existing_roi_indices,
        ignore_missing_regex=IGNORE_MISSING_REGEX,
        roi_select_first=ROI_SELECT_FIRST,  
        roi_separate=ROI_SEPARATE,
      )
      if mask is None: 
        msg = "No ROIs found in the RTSTRUCT."
        raise ValueError(msg)
      for name in mask.roi_indices:
        if name not in existing_roi_indices:
          existing_roi_indices[name] = len(existing_roi_indices)

      mask.existing_roi_indices = existing_roi_indices

      mask_arr = np.transpose(sitk.GetArrayFromImage(mask))
      if len(mask_arr.shape) == 3: # noqa
        mask_arr = mask_arr.reshape(1, mask_arr.shape[0], mask_arr.shape[1], mask_arr.shape[2])
      roi_names_list = list(mask.roi_indices.keys())
      for roi_idx in range(mask_arr.shape[0]):
        new_mask = sitk.GetImageFromArray(np.transpose(mask_arr[roi_idx]))
        new_mask.CopyInformation(mask)
        new_mask = Segmentation(new_mask)
        mask_to_process = new_mask

        # output
        output(
          subject_id=subject_id, 
          img=mask_to_process, 
          output_stream=output_stream, 
          is_mask=True, 
          mask_label=roi_names_list[roi_idx]
        )
    case _:
      logger.warning(f"Skipping modality: {modality}")
      continue


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



