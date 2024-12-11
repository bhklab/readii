from pathlib import Path

from rich import print as rprint

from readii.loaders import loadDicomSITK, loadRTSTRUCTSITK
from readii.negative_controls_refactor.manager import NegativeControlManager  # noqa
from readii.negative_controls_refactor.negative_controls import (
	RandomizedControl,
	SampledControl,  # noqa
	ShuffledControl,  # noqa
)  # noqa
from readii.negative_controls_refactor.regions import FullRegion, NonROIRegion, ROIRegion  # noqa

RANDOM_SEED = 10


def main() -> None:
	"""Test the negative_controls_refactor module."""
	################################################################################################
	# Load Data
	dataset_path = Path.cwd() / "tests" / "4D-Lung"

	ct_dir = (
		dataset_path
		/ "113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"
	)
	rtstruct_dir = (
		dataset_path
		/ "113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35"
	)
	rtstruct_file = next(rtstruct_dir.glob("*.dcm"))

	ct = loadDicomSITK(ct_dir)

	ROI_OF_INTEREST = "Tumor_c40"
	rt = loadRTSTRUCTSITK(rtstruct_file, ct_dir, roiNames=[ROI_OF_INTEREST]).get(ROI_OF_INTEREST)
	rprint(f"CT image: {ct.GetSize()}")
	rprint(f"RTSTRUCT image: {rt.GetSize()}")

	################################################################################################
	# Example usage of the negative control strategies
	################################################################################################

	# EXAMPLE 1: Using the concrete classes directly
	control_strategy = RandomizedControl(random_seed=RANDOM_SEED)
	region_strategy = ROIRegion()

	# this calls the `__call__` method of the NegativeControlStrategy class
	neg_image1 = control_strategy(image=ct, mask=rt, region=region_strategy)
	rprint(f"Negative control image 1: {neg_image1.GetSize()}")

	# EXAMPLE 2: alternatively, you can use them without instantiating the classes as variables
	neg_image2 = RandomizedControl(random_seed=RANDOM_SEED)(image=ct, mask=rt, region=ROIRegion())
	rprint(f"Negative control image 2: {neg_image2.GetSize()}")

	# EXAMPLE 3: Using the manager class and the `apply_single` method
	manager = (
		NegativeControlManager()
	)  # by default, uses 0 strategies and 0 regions, but can passed in as args

	neg_image3, control_strategy_name, region_strategy_name = manager.apply_single(
		base_image=ct,
		mask=rt,
		control_strategy="randomized",
		region_strategy="roi",
		random_seed=RANDOM_SEED,
	)
	rprint(
		f"Negative control image 3: {neg_image3.GetSize()} using {control_strategy_name} and {region_strategy_name}"
	)

	# EXAMPLE 4: Using manager, and combined string representations of the strategies
	manager_2 = NegativeControlManager.from_strings(
		negative_control_types=["randomized", "shuffled", "sampled"],
		region_types=["roi", "non_roi", "full"],
		random_seed=RANDOM_SEED,
	)
	rprint(f"There are {len(manager_2)} combinations of negative control and region strategies")
	rprint(manager_2)

	# Apply all combinations of negative control and region strategies
	for neg_image, control_strategy_name, region_strategy_name in manager_2.apply(ct, rt):
		rprint(
			f"Negative control image generated: {neg_image.GetSize()} using {control_strategy_name} and {region_strategy_name}"
		)


if __name__ == "__main__":
	main()
