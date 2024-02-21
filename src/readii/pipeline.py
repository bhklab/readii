from argparse import ArgumentParser
import os

from readii.metadata import *
from readii.feature_extraction import *

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

    return parser.parse_known_args()[0]
    

def main():
    """Function to run READII radiomic feature extraction pipeline.
    """
    args = parser()
    args_dict = vars(args)

    print("Starting readii pipeline...")

    # Set up output directory
    outputDir = os.path.join(args.output_directory, "readii_outputs")
    if not os.path.exists(outputDir):
        print("Creating output directory:", outputDir)
        os.makedirs(outputDir)

    # Find med-imagetools output files
    print("Finding med-imagetools outputs...")
    parentDirPath, datasetName = os.path.split(args.data_directory)
    imageFileListPath = os.path.join(parentDirPath + "/.imgtools/imgtools_" + datasetName + ".csv")
    if not os.path.exists(imageFileListPath):
        # Can we run med-imagetools in here?
        raise FileNotFoundError("Output for med-imagetools not found for this image set. Check the data_directory argument or run med-imagetools.")

    print("Getting segmentation type...")
    # Get segType from imageFileList to generate the image metadata file and set up feature extraction
    segType = getSegmentationType(imageFileListPath)

    # Check if image metadata file has already been created
    imageMetadataPath = os.path.join(outputDir, "ct_to_seg_match_list_" + datasetName + ".csv")
    if not os.path.exists(imageMetadataPath) or args.update:
        print("Matching CT to segmentations...")
        # Generate image metadata file by matching CT and segmentations in imageFileList from med-imagetools
        matchCTtoSegmentation(imgFileListPath = imageFileListPath,
                              segType = segType,
                              outputDirPath = outputDir)
    else:
        print("Image metadata file has already been created.")
    
    # Check if radiomic feature file already exists
    radFeatOutPath = os.path.join(outputDir, "features/", "radiomicfeatures_" + datasetName + ".csv")
    if not os.path.exists(radFeatOutPath) or args.update:
        print("Starting radiomic feature extraction...")
        radiomicFeatures = radiomicFeatureExtraction(imageMetadataPath = imageMetadataPath,
                                                     imageDirPath = parentDirPath,
                                                     roiNames = args.roi_names,
                                                     pyradiomicsParamFilePath = args.pyradiomics_setting,
                                                     outputDirPath = outputDir,
                                                     negativeControl = None,
                                                     parallel = args.parallel)
    else:
        print("Radiomic features have already been extracted. See ", radFeatOutPath,)

    # Negative control radiomic feature extraction
    if args.negative_controls != None:
        # Get all negative controls to run
        negativeControlList = args.negative_controls.split(",")

        # Perform feature extraction for each negative control type
        for negativeControl in negativeControlList:
            ncRadFeatOutPath = os.path.join(outputDir, "features/", "radiomicfeatures_" + negativeControl + "_" + datasetName + ".csv")
            if not os.path.exists(ncRadFeatOutPath) or args.update:
                print("Starting radiomic feature extraction for negative control: ", negativeControl)
                ncRadiomicFeatures = radiomicFeatureExtraction(imageMetadataPath = imageMetadataPath,
                                                               imageDirPath = parentDirPath,
                                                               roiNames = args.roi_names,
                                                               pyradiomicsParamFilePath = args.pyradiomics_setting,
                                                               outputDirPath = outputDir,
                                                               negativeControl = negativeControl,
                                                               parallel = args.parallel)
            else:
                print(negativeControl, " radiomic features have already been extracted. See ", ncRadFeatOutPath)

    
    print("Pipeline complete.")

if __name__ == "__main__":
    main()