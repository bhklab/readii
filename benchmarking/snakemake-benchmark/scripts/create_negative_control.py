from email.mime import base
from readii.loaders import loadDicomSITK, loadSegmentation

from readii.negative_controls import (
    applyNegativeControl
)

import SimpleITK as sitk

ct_img_dir = snakemake.input["ct_img_dir"]
seg_dcm_path = snakemake.input["seg_dcm_path"]

negative_control = snakemake.params["negative_control"]
roiLabel = snakemake.params["roiLabel"]
modality = snakemake.params["modality"]


result = applyNegativeControl(
    nc_type = negative_control,
    baseImage = loadDicomSITK(imgDirPath=ct_img_dir),
    baseROI = loadSegmentation(
        segImagePath=seg_dcm_path, 
        modality = modality, 
        baseImageDirPath = ct_img_dir
        )['Tumor_c40'],
    roiLabel = roiLabel,
)

# save itk image somehow??? 
# save the image
output = snakemake.output["output_sitk_image"]


