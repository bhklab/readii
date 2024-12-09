from pathlib import Path

import click
from pydicom import dcmread


@click.command()
@click.argument(
	"input_path",
	type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False),
)
def main(input_path: Path) -> None:
	"""Extract ROI names from RTSTRUCT file."""
	rtstruct = dcmread(input_path, stop_before_pixels=True, specific_tags=['StructureSetROISequence', 'Modality'])
	assert rtstruct.Modality == "RTSTRUCT", "Input file is not an RTSTRUCT file."
	roi_names = [roi.ROIName for roi in rtstruct.StructureSetROISequence]
	sorted_roi_names = sorted(roi_names)
	for roi in sorted_roi_names:
		click.echo(roi)

if __name__ == "__main__":
	main()