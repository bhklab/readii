from argparse import ArgumentParser
from ast import arg
from pathlib import Path

from readii.utils.logging_config import get_logger  # Updated import
from readii.metadata import createImageMetadataFile, getSegmentationType
from readii.feature_extraction import radiomicFeatureExtraction


def parser():
    """Function to take command-line arguments and set them up for the pipeline run"""
    parser = ArgumentParser("READII Feature Extraction Pipeline")

    # Required arguments
    parser.add_argument(
        "data_directory",
        type=str,
        help="Path to top-level directory of image dataset. Same as med-imagetools.",
    )

    parser.add_argument(
        "output_directory",
        type=str,
        help="Path to output directory to save radiomic features and metadata.",
    )

    # Create a separate argument group for options
    options_group = parser.add_argument_group("Options")
    options_group.add_argument(
        "--roi_names",
        type=str,
        default=None,
        help="Name of region of interest in RTSTRUCT to perform extraction on.",
    )

    options_group.add_argument(
        "--pyradiomics_setting",
        type=str,
        default=None,
        help="Path to PyRadiomics configuration YAML file. If none provided, will use \
                                     default in src/readii/data/.",
    )

    options_group.add_argument(
        "--negative_controls",
        type=str,
        default=None,
        help="List of negative control types to run feature extraction on. Input as comma-separated list with no spaces.  \
                                     Options: randomized_full,randomized_roi,randomized_non_roi,shuffled_full,shuffled_roi,shuffled_non_roi,randomized_sampled_full,randomized_sampled_roi,randomized_sampled_non_roi",
    )

    options_group.add_argument(
        "--parallel",
        action="store_true",
        help="Whether to run feature extraction in a parallel process. False by default.",
    )

    options_group.add_argument(
        "--update",
        action="store_true",
        help="Flag to force rerun all steps of pipeline. False by default.",
    )

    options_group.add_argument(
        "--random_seed",
        type=int,
        help="Value to set random seed to for reproducible negative controls",
    )

    options_group.add_argument(
        "--keep_running",
        action="store_true",
        help="Flag to keep pipeline running even when feature extraction for a patient fails. False by default.",
    )

    # Create a separate argument group for logging configuration
    log_group = parser.add_argument_group("Logging Configuration")
    log_group.add_argument(
        "--log_file",
        type=str,
        default="readii.log",
        help=(
            "The path to the log file. This can be an absolute path or a relative path."
            "If the path is an absolute path, but a directory, the log file will be created in that directory with the name 'readii.log'. "
            "If the path is a relative path, the log file will be created in the current working directory under a 'logs' directory. "
            "If the path does not have a '.log' suffix, it will be added automatically. Default is 'readii.log'."
        ),
    )

    log_group.add_argument(
        "--log_level",
        type=str,
        default="DEBUG",
        help=(
            "The logging level. This can be one of the standard logging levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'. "
            "Default is 'DEBUG'."
        ),
    )

    return parser.parse_known_args()[0]


def main():
    """Function to run READII radiomic feature extraction pipeline."""
    args = parser()

    # Configure logger with user-defined log file name and log level
    logger = get_logger(logfile_path=args.log_file, level=args.log_level, handlers=["console", "file", "json"])

    logger.info("Starting readii pipeline...",args=vars(args))

    # Set up output directory
    outputDir = Path(args.output_directory) / "readii_outputs"
    if not outputDir.exists():
        logger.info(f"Directory {outputDir} does not exist. Creating...")
        outputDir.mkdir(parents=True, exist_ok=True)
    else:
        logger.warning(
            f"Directory {outputDir} already exists. Will overwrite contents."
        )

    # Find med-imagetools output files
    logger.info("Finding med-imagetools outputs...")
    data_dir = Path(args.data_directory)
    assert data_dir.exists(), f"Data directory {data_dir} does not exist."
    parentDirPath = data_dir.parent
    datasetName = data_dir.name
    imageFileListPath = parentDirPath / f".imgtools/imgtools_{datasetName}.csv"
    if not imageFileListPath.exists():
        # Can we run med-imagetools in here?
        logger.exception(
            f"Expected file {imageFileListPath} not found. Check the data_directory argument or run med-imagetools."
        )
        raise FileNotFoundError(
            "Output for med-imagetools not found for this image set. Check the data_directory argument or run med-imagetools."
        )

    logger.info("Getting segmentation type...")
    try:
        # Get segType from imageFileList to generate the image metadata file and set up feature extraction
        segType = getSegmentationType(imageFileListPath.as_posix())
    except RuntimeError as e:
        logger.exception("Could not get segmentation type.")
        exit()

    # Check if image metadata file has already been created
    imageMetadataPath = createImageMetadataFile(
        outputDir, parentDirPath, datasetName, segType, imageFileListPath, args.update
    )

    # Check if radiomic feature file already exists
    radFeatOutPath = (
        outputDir / "features" / f"radiomicfeatures_original_{datasetName}.csv"
    )
    try:
        if not radFeatOutPath.exists() or args.update:
            logger.info("Starting radiomic feature extraction...")
            radiomicFeatures = radiomicFeatureExtraction(
                imageMetadataPath=imageMetadataPath.as_posix(),
                imageDirPath=parentDirPath,
                roiNames=args.roi_names,
                pyradiomicsParamFilePath=args.pyradiomics_setting,
                outputDirPath=outputDir,
                negativeControl=None,
                parallel=args.parallel,
                keep_running=args.keep_running,
            )
        else:
            logger.info(
                f"Radiomic features have already been extracted. See {radFeatOutPath}"
            )

        # Negative control radiomic feature extraction
        if args.negative_controls != None:
            # Get all negative controls to run
            negativeControlList = args.negative_controls.split(",")

            # Perform feature extraction for each negative control type
            for negativeControl in negativeControlList:
                ncRadFeatOutPath = (
                    outputDir
                    / "features"
                    / f"radiomicfeatures_{negativeControl}_{datasetName}.csv"
                )
                if not ncRadFeatOutPath.exists() or args.update:
                    logger.info(
                        f"Starting radiomic feature extraction for negative control: {negativeControl}"
                    )
                    ncRadiomicFeatures = radiomicFeatureExtraction(
                        imageMetadataPath=imageMetadataPath.as_posix(),
                        imageDirPath=parentDirPath,
                        roiNames=args.roi_names,
                        pyradiomicsParamFilePath=args.pyradiomics_setting,
                        outputDirPath=outputDir,
                        negativeControl=negativeControl,
                        randomSeed=args.random_seed,
                        parallel=args.parallel,
                        keep_running=args.keep_running,
                    )
                else:
                    logger.info(
                        f"{negativeControl} radiomic features have already been extracted. See {ncRadFeatOutPath}"
                    )
    except Exception as e:
        logger.exception(f"Error running radiomic feature extraction: {e}")
        exit()

    logger.info("Pipeline complete.")


if __name__ == "__main__":
    main()
