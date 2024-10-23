"""CLI Tool for Applying Negative Controls to Radiomics Images."""

from itertools import product
from pathlib import Path
from typing import List, Optional

import click

from readii.negative_controls.base import NegativeControl
from readii.negative_controls.enums import NegativeControlRegion
from readii.negative_controls.factory import NegativeControlFactory
from readii.negative_controls.registry import NegativeControlRegistry

def negative_control_types() -> List[str]:
    """Return a list of all registered negative control types.

    A Negative Control is made up of a type and a region.
    This function returns a list of all combinations of types and regions.

    """
    # Get all registered negative control types
    negative_control_types = NegativeControlRegistry.get_control_types()

    # Get all region names from the enum
    regions = [e.name for e in NegativeControlRegion]

    # Use itertools.product to create combinations
    return [f"{nc_type}_{region}" for nc_type, region in product(negative_control_types, regions)]


def parse_negative_controls(ctx, param, value) -> list: # noqa: ANN001, ANN201
    """Parse the negative controls input, allowing comma-separated and multiple uses.

    Raises an error if duplicate values are detected.
    """
    if not value:
        return []

    # Flatten out and split any comma-separated values
    controls = []
    for item in value:
        controls.extend(item.split(","))

    # Check for duplicates
    seen = set()
    duplicates = {x for x in controls if x in seen or seen.add(x)}
    if duplicates:
        raise click.BadParameter(
            f"\n\tDuplicate negative controls detected: {', '.join(duplicates)}"
        )

    return controls


@click.group(context_settings={'help_option_names': ['-h', '--help']},)
def cli() -> None:
    """CLI Tool for Applying Negative Controls to Radiomics Images."""
    pass


@cli.command()
@click.argument(
    "base_image_path",
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True,
        path_type=Path,
        resolve_path=True,
    ),
)
@click.option(
    "--roi-mask-path",
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
        resolve_path=True,
    ),
    default=None,
    help="Path to the ROI mask image (optional).",
)
@click.option(
    "--negative-controls",
    "--nc",
    multiple=True,
    callback=parse_negative_controls,
    help="Negative control types to apply (multiple). subcommand list_controls for options.",
)
@click.option("--random-seed", type=int, default=None, help="Random seed for reproducibility.")
def apply(
    base_image_path: Path,
    roi_mask_path: Optional[Path],
    negative_controls: Optional[List[str]],
    random_seed: Optional[int],
) -> None:
    """Example CLI tool for applying negative controls to radiomics images.

    Example!: All this does is print out the arguments passed in for now.
    BASE_IMAGE_PATH: The path to the base image file.

    """ # noqa: D401
    print(
        f"You passed in BASE_IMAGE_PATH: {base_image_path},\n"
        f"You passed in ROI_MASK_PATH: {roi_mask_path},\n"
        f"You passed in NEGATIVE_CONTROLS: {negative_controls},\n"
        f"You passed in RANDOM_SEED: {random_seed}"
    )



@cli.command()
def list_controls() -> None:
    """List all registered negative control types."""
    print(f"{negative_control_types()}")

if __name__ == "__main__":
    cli()
