import click
from orcestradownloader.cli import DatasetMultiCommand
from orcestradownloader.dataset_config import DATASET_CONFIG
from orcestradownloader.managers import DatasetManager, DatasetRegistry

# only register the 'radiomicsets' dataset

DATASET_TYPE = "radiomicsets"

readii_registry = DatasetRegistry()
readii_registry.register(
	DATASET_TYPE,
	DatasetManager(
		url=DATASET_CONFIG[DATASET_TYPE].url,
		cache_file=DATASET_CONFIG[DATASET_TYPE].cache_file,
		dataset_type=DATASET_CONFIG[DATASET_TYPE].dataset_type,
	),
)


@click.command(
	name="readii-datasets",
	cls=DatasetMultiCommand,
	registry=readii_registry,
	invoke_without_command=True,
)
@click.help_option("-h", "--help", help="Show this message and exit.")
@click.pass_context
def cli(ctx: click.Context) -> None:
	"""Interact with datasets on orcestra.ca."""
	ctx.ensure_object(dict)

	# if no subcommand is provided, print help
	if ctx.invoked_subcommand is None:
		click.echo(ctx.get_help())
		return


if __name__ == "__main__":
	cli()
