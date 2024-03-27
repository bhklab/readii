from readii.loaders import loadDicomSITK, loadSegmentation
from readii.image_processing import flattenImage, alignImages, displayImageSlice, displayCTSegOverlay
from readii.negative_controls import (
    applyNegativeControl,
    shuffleImage, 
    makeRandomImage,
    makeRandomRoi,
    shuffleROI,
    makeRandomNonRoi,
    shuffleNonROI,
    randomizeImageFromDistribtutionSampling,
    makeRandomFromRoiDistribution,
    makeRandomNonRoiFromDistribution,
)


ct_img_dir = snakemake.input["ct_img_dir"]
seg_dcm_path = snakemake.input["seg_dcm_path"]

negative_control = snakemake.params["negative_control"]
roiLabel = snakemake.params["roiLabel"]

result = applyNegativeControl(
    nc_type = negative_control,
    baseImage = loadDicomSITK(ct_img_dir),
    roiImage = loadSegmentation(seg_dcm_path),
    roiLabel = roiLabel,
)

# save itk image somehow??? 
# save the image
output = snakemake.output["output_sitk_image"]


