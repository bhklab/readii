from argparse import ArgumentParser
from ast import arg
import os
from venv import logger

from readii.metadata import *
from readii.feature_extraction import *
from readii.utils import get_logger

logger = get_logger()

def parser():
    """Function to take command-line arguments and set them up for the pipeline run
    """
    parser = ArgumentParser("READII Feature Extraction Pipeline")

    # arguments
    parser.add_argument("data_directory", type=str,
                        help="Path to top-level directory of image dataset. Same as med-imagetools.")
    
    parser.add_argument("output_directory", type=str,
                       help="Path to output directory to save radiomic features and metadata.")
    
    parser.add_argument("--roi_names", type=str, default=None,
                        help="Name of region of interest in RTSTRUCT to perform extraction on.")
    
    parser.add_argument("--pyradiomics_setting", type=str, default=None,
                        help="Path to PyRadiomics configuration YAML file. If none provided, will use \
                              default in src/readii/data/.")
    
    parser.add_argument("--negative_controls", type=str, default=None,
                        help="List of negative control types to run feature extraction on. Input as comma-separated list with no spaces.  \
                              Options: randomized_full,randomized_roi,randomized_non_roi,shuffled_full,shuffled_roi,shuffled_non_roi,randomized_sampled_full,randomized_sampled_roi,randomized_sampled_non_roi")

    parser.add_argument("--parallel", action="store_true",
                        help="Whether to run feature extraction in a parallel process. False by default.")

    parser.add_argument("--update", action="store_true", help="Flag to force rerun all steps of pipeline. False by default.")

    parser.add_argument("--random_seed", type=int,
                        help="Value to set random seed to for reproducible negative controls")

    return parser.parse_known_args()[0]
    

    

def main():
    """Function to run READII radiomic feature extraction pipeline.
    """
    args = parser()
    pretty_args = '\n\t'.join([f"{k}: {v}" for k, v in vars(args).items()])
    logger.debug(
        f"Arguments:\n\t{pretty_args}"
    )
    
    args_dict = vars(args)

    logger.info("Starting readii pipeline...")

    # Set up output directory
    outputDir = os.path.join(args.output_directory, "readii_outputs")
    if not os.path.exists(outputDir):
        logger.info(f"Directory {outputDir} does not exist. Creating...")
        os.makedirs(outputDir)
    else:
        logger.warning(f"Directory {outputDir} already exists. Will overwrite contents.")

    # Find med-imagetools output files
    logger.info("Finding med-imagetools outputs...")
    parentDirPath, datasetName = os.path.split(args.data_directory)
    imageFileListPath = os.path.join(parentDirPath + "/.imgtools/imgtools_" + datasetName + ".csv")
    if not os.path.exists(imageFileListPath):
        # Can we run med-imagetools in here?
        logger.error(
            f"Expected file {imageFileListPath} not found. Check the data_directory argument or run med-imagetools."
        )
        raise FileNotFoundError("Output for med-imagetools not found for this image set. Check the data_directory argument or run med-imagetools.")

    logger.info("Getting segmentation type...")
    try:
        # Get segType from imageFileList to generate the image metadata file and set up feature extraction
        segType = getSegmentationType(imageFileListPath)
    except RuntimeError as e:
        logger.error(str(e))
        logger.error("Feature extraction not complete.")
        exit()


    # Check if image metadata file has already been created
    imageMetadataPath = createImageMetadataFile(
        outputDir, 
        parentDirPath, 
        datasetName, 
        segType, 
        imageFileListPath, 
        args.update)
    
    # Check if radiomic feature file already exists
    radFeatOutPath = os.path.join(outputDir, "features/", "radiomicfeatures_original_" + datasetName + ".csv")
    if not os.path.exists(radFeatOutPath) or args.update:
        logger.info("Starting radiomic feature extraction...")
        radiomicFeatures = radiomicFeatureExtraction(imageMetadataPath = imageMetadataPath,
                                                     imageDirPath = parentDirPath,
                                                     roiNames = args.roi_names,
                                                     pyradiomicsParamFilePath = args.pyradiomics_setting,
                                                     outputDirPath = outputDir,
                                                     negativeControl = None,
                                                     parallel = args.parallel)
    else:
        logger.info(f"Radiomic features have already been extracted. See {radFeatOutPath}")

    # Negative control radiomic feature extraction
    if args.negative_controls != None:
        # Get all negative controls to run
        negativeControlList = args.negative_controls.split(",")

        # Perform feature extraction for each negative control type
        for negativeControl in negativeControlList:
            ncRadFeatOutPath = os.path.join(outputDir, "features/", "radiomicfeatures_" + negativeControl + "_" + datasetName + ".csv")
            if not os.path.exists(ncRadFeatOutPath) or args.update:
                logger.info(f"Starting radiomic feature extraction for negative control: {negativeControl}")
                ncRadiomicFeatures = radiomicFeatureExtraction(imageMetadataPath = imageMetadataPath,
                                                               imageDirPath = parentDirPath,
                                                               roiNames = args.roi_names,
                                                               pyradiomicsParamFilePath = args.pyradiomics_setting,
                                                               outputDirPath = outputDir,
                                                               negativeControl = negativeControl,
                                                               randomSeed=args.random_seed,
                                                               parallel = args.parallel)
            else:
                logger.info(f"{negativeControl} radiomic features have already been extracted. See {ncRadFeatOutPath}")

    
    logger.info("Pipeline complete.")

if __name__ == "__main__":
    main()