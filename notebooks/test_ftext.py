from readii.loaders import (
    loadDicomSITK,
    loadRTSTRUCTSITK,
    loadSegmentation,
)

from readii.feature_extraction import (
    singleRadiomicFeatureExtraction,
    radiomicFeatureExtraction,
)

import pytest
import collections
import pandas as pd
import os
import radiomics
from readii.utils import get_logger

# @pytest.fixture
# def nsclcCTImage():
#     nsclcCTPath = "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"
#     return loadDicomSITK(nsclcCTPath)


# @pytest.fixture
# def nsclcSEGImage():
#     nsclcSEGPath = "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/1000.000000-3D_Slicer_segmentation_result-67652/1-1.dcm"
#     segDictionary = loadSegmentation(nsclcSEGPath, modality = 'SEG')
#     return segDictionary['Heart']
def pyradiomicsParamFilePath():
    return "src/readii/data/default_pyradiomics.yaml"


def lung4DCTImage():
    lung4DCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"
    return loadDicomSITK(lung4DCTPath)


def lung4DRTSTRUCTImage():
    lung4DRTSTRUCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-47.35/1-1.dcm"
    lung4DCTPath = "tests/4D-Lung/113_HM10395/11-26-1999-NA-p4-13296/1.000000-P4P113S303I10349 Gated 40.0B-29543"
    segDictionary = loadSegmentation(
        lung4DRTSTRUCTPath,
        modality="RTSTRUCT",
        baseImageDirPath=lung4DCTPath,
        roiNames="Tumor_c.*",
    )
    return segDictionary["Tumor_c40"]


if __name__ == "__main__":
    ct = lung4DCTImage()
    seg = lung4DRTSTRUCTImage()
    import logging
    

    logger = get_logger()
    # globally defined formatter exists called 'json'
    
    radiomics_logger = radiomics.logger
    radiomics_logger.handlers.clear()
    for handler in logger.handlers:
        radiomics_logger.addHandler(handler)


    actual = singleRadiomicFeatureExtraction(ct, seg, pyradiomicsParamFilePath())
