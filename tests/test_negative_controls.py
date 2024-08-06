import numpy as np

from readii.image_processing import *
from radiomics import imageoperations
from readii.negative_controls import (
    makeShuffleImage,
    makeRandomImage,
    makeRandomSampleFromDistributionImage,
    negativeControlROIOnly,
    negativeControlNonROIOnly,
    applyNegativeControl
)


import pytest
import collections


@pytest.fixture
def nsclcCTImage():
    nsclcCTPath = "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"
    return loadDicomSITK(nsclcCTPath)


@pytest.fixture
def nsclcSEGImage():
    nsclcSEGPath = "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/1000.000000-3D_Slicer_segmentation_result-67652/1-1.dcm"
    segDictionary = loadSegmentation(nsclcSEGPath, modality='SEG')
    return segDictionary['Heart']


@pytest.fixture()
def nsclcCTImageFolderPath():
    return "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"


@pytest.fixture()
def nsclcSEGFilePath():
    return "tests/NSCLC_Radiogenomics/R01-001/09-06-1990-NA-CT_CHEST_ABD_PELVIS_WITH_CON-98785/3.000000-THORAX_1.0_B45f-95741"


@pytest.fixture()
def nsclcCropped(nsclcCTImage, nsclcSEGImage, nsclcCTImageFolderPath, nsclcSEGFilePath):
    roiImage = flattenImage(nsclcSEGImage)
    alignedROIImage = alignImages(nsclcCTImage, roiImage)
    segmentationLabel = getROIVoxelLabel(alignedROIImage)

    croppedCT, croppedROI = getCroppedImages(nsclcCTImage, alignedROIImage, segmentationLabel)

    return croppedCT, croppedROI, segmentationLabel


@pytest.fixture()
def randomSeed():
    return 10

def test_makeShuffleImage(nsclcCTImage, randomSeed):
    " Test negative control to shuffle the whole image"

    shuffled_image = makeShuffleImage(nsclcCTImage, randomSeed)
    original_pixels = sitk.GetArrayFromImage(nsclcCTImage)
    shuffled_pixels = sitk.GetArrayFromImage(shuffled_image)

    assert nsclcCTImage.GetSize() == shuffled_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert nsclcCTImage.GetSpacing() == shuffled_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert nsclcCTImage.GetOrigin() == shuffled_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_pixels), \
        "Pixel values are not shuffled"
    assert np.array_equal(np.sort(original_pixels.flatten()),
                          np.sort(shuffled_pixels.flatten())), \
        "Shuffled image has different pixel values than original image. Should just be original pixels rearranged."
    assert shuffled_pixels[0,0,0] == -987, \
        "Random seed is not working for shuffled image, first voxel has wrong shuffled value. Random seed should be 10."
    assert shuffled_pixels[-1,-1,-1] == 10, \
        "Random seed is not working for shuffled image, last voxel has wrong shuffled value. Random seed should be 10."
    assert shuffled_pixels[238,252,124] == -118, \
        "Random seed is not working for shuffled image, central ROI voxel has wrong shuffled value. Random seed should be 10."


def test_makeRandomImage(nsclcCTImage, randomSeed):
    " Test negative control to randomize the pixels of the whole image"

    randomized_image = makeRandomImage(nsclcCTImage, randomSeed)
    original_arr_image = sitk.GetArrayFromImage(nsclcCTImage)
    minVoxelVal, maxVoxelVal = np.min(original_arr_image), np.max(original_arr_image)

    randomized_arr_image = sitk.GetArrayFromImage(randomized_image)

    assert nsclcCTImage.GetSize() == randomized_image.GetSize(), \
        "Randomized image size not same as input image"
    assert nsclcCTImage.GetSpacing() == randomized_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert nsclcCTImage.GetOrigin() == randomized_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert randomized_arr_image.max() <= maxVoxelVal and randomized_arr_image.min() >= minVoxelVal, \
        "Pixel values are not within the expected range"
    assert randomized_arr_image[0,0,0] == 2156, \
        "Random seed is not working for random image, first voxel has wrong random value. Random seed should be 10."
    assert randomized_arr_image[-1,-1,-1] == 90, \
        "Random seed is not working for random image, last voxel has wrong random value. Random seed should be 10."
    assert randomized_arr_image[238,252,124] == -840, \
        "Random seed is not working for random image, central ROI voxel has wrong random value. Random seed should be 10."
    

def test_makeRandomSampleFromDistributionImage(nsclcCTImage, randomSeed):
    " Test negative control to uniformly sample the pixels of the whole image from the images pixel distribution"

    randomized_sampled_image = makeRandomSampleFromDistributionImage(nsclcCTImage, randomSeed)
    original_arr_image = sitk.GetArrayFromImage(nsclcCTImage)

    randomized_arr_image = sitk.GetArrayFromImage(randomized_sampled_image)

    assert nsclcCTImage.GetSize() == randomized_sampled_image.GetSize(), \
        "Randomized sampled image size not same as input image"
    assert nsclcCTImage.GetSpacing() == randomized_sampled_image.GetSpacing(), \
        "Randomized sampled image spacing not same as input image"
    assert nsclcCTImage.GetOrigin() == randomized_sampled_image.GetOrigin(), \
        "Randomized sampled image origin not same as input image"
    assert isinstance(randomized_sampled_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_arr_image, randomized_arr_image), \
        "No voxel values have been changed to random."
    assert np.all(np.isin(randomized_arr_image.flatten(), original_arr_image.flatten())), \
        "Retuned object has values not sampled from original image"
    assert randomized_arr_image[0,0,0] == -1005, \
        "Random seed is not working for randomized from distribution image, first voxel has wrong random value. Random seed should be 10."
    assert randomized_arr_image[-1,-1,-1] == 414, \
        "Random seed is not working for randomized from distribution image, last voxel has wrong random value. Random seed should be 10."
    assert randomized_arr_image[238,252,124] == 49, \
        "Random seed is not working for randomized from distribution image, central ROI voxel has wrong random value. Random seed should be 10."



def test_makeShuffleROI(nsclcCropped, randomSeed):
    " Test negative control to shuffle the roi of the image"

    croppedCT, croppedROI, _ = nsclcCropped

    shuffled_roi_image = negativeControlROIOnly(croppedCT, croppedROI, "shuffled", randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    shuffled_roi_pixels = sitk.GetArrayFromImage(shuffled_roi_image)

    assert croppedCT.GetSize() == shuffled_roi_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert croppedCT.GetSpacing() == shuffled_roi_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert croppedCT.GetOrigin() == shuffled_roi_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_roi_pixels), \
        "No voxel values are being shuffled."
    assert np.array_equal(np.sort(original_pixels.flatten()),
                          np.sort(shuffled_roi_pixels.flatten())), \
        "Shuffled pixel values in ROI are different"
    assert shuffled_roi_pixels[0,0,0] == -740, \
        "Voxel outside the ROI is being shuffled. Should just be the ROI voxels."
    assert shuffled_roi_pixels[7,18,11] == -322, \
        "Random seed is not working for shuffled ROI image, centre pixel has wrong value. Random seed should be 10."


def test_makeRandomROI(nsclcCropped, randomSeed):
    " Test negative control to randomize the pixels of the ROI of the image"

    croppedCT, croppedROI, _ = nsclcCropped

    randomized_roi_image = negativeControlROIOnly(croppedCT, croppedROI, "randomized", randomSeed)
    original_arr_image = sitk.GetArrayFromImage(croppedCT)
    minVoxelVal, maxVoxelVal = np.min(original_arr_image), np.max(original_arr_image)

    randomized_arr_image = sitk.GetArrayFromImage(randomized_roi_image)

    assert croppedCT.GetSize() == randomized_roi_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_roi_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_roi_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_arr_image, randomized_roi_image), \
        "No voxel values have been changed to random."
    assert randomized_arr_image.max() <= maxVoxelVal and randomized_arr_image.min() >= minVoxelVal, \
        "Pixel values are not within the expected range"
    assert randomized_arr_image[0,0,0] == -740, \
        "Voxel outside the ROI is being randomized. Should just be the ROI voxels."
    assert randomized_arr_image[7,18,11] == 1, \
        "Random seed is not working for randomized ROI image, centre pixel has wrong value. Random seed should be 10."


def test_makeRandomSampleFromDistributionROI(nsclcCropped, randomSeed):
    " Test negative control to uniformly sample the pixels of the ROI of the image randomly"

    croppedCT, croppedROI, _= nsclcCropped

    randomized_roi_image = negativeControlROIOnly(croppedCT, croppedROI, "randomized_sampled", randomSeed)
    original_arr_image = sitk.GetArrayFromImage(croppedCT)

    randomized_roi_arr_image = sitk.GetArrayFromImage(randomized_roi_image)

    assert croppedCT.GetSize() == randomized_roi_image.GetSize(), \
        "Randomized ROI Sampled image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_roi_image.GetSpacing(), \
        "Randomized ROI Sampled image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_roi_image.GetOrigin(), \
        "Randomized ROI Sampled image origin not same as input image"
    assert isinstance(randomized_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_arr_image, randomized_roi_arr_image), \
        "No voxel values have been changed to random."
    assert np.all(np.isin(randomized_roi_arr_image.flatten(), original_arr_image.flatten())), \
        "Retuned object has values not sampled from original image"
    assert randomized_roi_arr_image[0,0,0] == -740, \
        "Voxel outside the ROI is being randomized. Should just be the ROI voxels."
    assert randomized_roi_arr_image[7,18,11] == -81, \
        "Random seed is not working for randomized from distribution ROI image, centre pixel has wrong value. Random seed should be 10."
    

def test_makeShuffleNonROI(nsclcCropped, randomSeed):
    " Test negative control to shuffle the pixels outside roi of the image"

    croppedCT, croppedROI, _ = nsclcCropped

    shuffled_non_roi_image = negativeControlNonROIOnly(croppedCT, croppedROI, "shuffled", randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    shuffled_non_roi_pixels = sitk.GetArrayFromImage(shuffled_non_roi_image)

    assert croppedCT.GetSize() == shuffled_non_roi_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert croppedCT.GetSpacing() == shuffled_non_roi_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert croppedCT.GetOrigin() == shuffled_non_roi_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_non_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_non_roi_pixels), \
        "Shuffled image has different pixel values than original image. Should just be original pixels rearranged."
    assert np.array_equal(np.sort(original_pixels.flatten()),
                          np.sort(shuffled_non_roi_pixels.flatten())), \
        "Shuffled pixel values outside ROI are different"
    assert shuffled_non_roi_pixels[0,0,0] == -840, \
        "Random seed is not working for shuffled non-ROI image, first voxel has wrong shuffle value. Random seed should be 10."
    assert shuffled_non_roi_pixels[-1,-1,-1] == -490, \
        "Random seed is not working for shuffled non-ROI image, last voxel has wrong shuffle value. Random seed should be 10."
    assert shuffled_non_roi_pixels[7,18,11] == -1, \
        "ROI is getting shuffled when it shouldn't."


def test_makeRandomNonRoi(nsclcCropped, randomSeed):
    " Test negative control to randomize the pixels outside the ROI of the image"

    croppedCT, croppedROI, _ = nsclcCropped

    randomized_non_roi_image = negativeControlNonROIOnly(croppedCT, croppedROI, "randomized", randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    randomized_non_roi_pixels = sitk.GetArrayFromImage(randomized_non_roi_image)

    # Make ROI pixels = NaN to help check of min and max values in non-ROI pixels
    original_roi_pixels = sitk.GetArrayFromImage(croppedROI)
    roiMask = np.where(original_roi_pixels > 0, np.NaN, 1)
    masked_randomized_non_roi_pixels = randomized_non_roi_pixels * roiMask
    
    assert croppedCT.GetSize() == randomized_non_roi_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_non_roi_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_non_roi_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_non_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert np.nanmax(masked_randomized_non_roi_pixels) <= np.max(original_pixels) and np.nanmin(masked_randomized_non_roi_pixels) >= np.min(original_pixels), \
        "Pixel values outside ROI are not within the expected range"
    assert randomized_non_roi_pixels[0,0,0] == -124, \
        "Random seed is not working for randomized non-ROI image, first voxel has wrong random value. Random seed should be 10."
    assert randomized_non_roi_pixels[-1,-1,-1] == 123, \
        "Random seed is not working for randomized non-ROI image, last voxel has wrong random value. Random seed should be 10."
    assert randomized_non_roi_pixels[7,18,11] == -1, \
        "ROI is getting randomized when it shouldn't."


def test_makeRandomNonRoiFromDistribution(nsclcCropped, randomSeed):
    " Test negative control to randomize the pixels outside the ROI of the image"

    croppedCT, croppedROI, _ = nsclcCropped

    randomized_non_roi_image = negativeControlNonROIOnly(croppedCT, croppedROI, "randomized_sampled", randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    randomized_non_roi_pixels = sitk.GetArrayFromImage(randomized_non_roi_image)

    assert croppedCT.GetSize() == randomized_non_roi_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_non_roi_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_non_roi_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_non_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, randomized_non_roi_pixels), \
        "No voxel values have been changed to random."
    assert np.all(np.isin(randomized_non_roi_pixels, original_pixels)), \
        "Retuned object has values outside ROI not sampled from original image"
    assert randomized_non_roi_pixels[0,0,0] == -653, \
        "Random seed is not working for randomized from distribution non-ROI image. Random seed should be 10."
    assert randomized_non_roi_pixels[-1,-1,-1] == -805, \
        "Random seed is not working for randomized from distribution non-ROI image. Random seed should be 10."
    assert randomized_non_roi_pixels[7,18,11] == -1, \
        "ROI is getting randomized when it shouldn't."
    

@pytest.mark.parametrize(
    "wrongNCType",
    [
        "shaken",
        "stirred",
        ""
    ]
)
def test_negativeControlROIOnly_wrongNCType(nsclcCropped, wrongNCType):
    " Test passing wrong negative control type to negativeControlROIOnly"

    croppedCT, croppedROI, _ = nsclcCropped

    with pytest.raises(ValueError):
        negativeControlROIOnly(croppedCT, croppedROI, wrongNCType, randomSeed=10)


@pytest.mark.parametrize(
    "wrongNCType",
    [
        "shaken",
        "stirred",
        ""
    ]
)
def test_negativeControlNonROIOnly_wrongNCType(nsclcCropped, wrongNCType):
    " Test passing wrong negative control type to negativeControlNonROIOnly"

    croppedCT, croppedROI, _ = nsclcCropped

    with pytest.raises(ValueError):
        negativeControlNonROIOnly(croppedCT, croppedROI, wrongNCType, randomSeed=10)


# def test_noROILabel_shuffleROI(nsclcCropped, randomSeed):
#     " Test passing no roiLabel to shuffleROI"

#     croppedCT, croppedROI, _ = nsclcCropped

#     shuffled_roi_image = negativeControlROIOnly(croppedCT, croppedROI, randomSeed=randomSeed)

#     original_pixels = sitk.GetArrayFromImage(croppedCT)
#     shuffled_roi_pixels = sitk.GetArrayFromImage(shuffled_roi_image)

#     assert croppedCT.GetSize() == shuffled_roi_image.GetSize(), \
#         "Shuffled image size not same as input image"
#     assert croppedCT.GetSpacing() == shuffled_roi_image.GetSpacing(), \
#         "Shuffled image spacing not same as input image"
#     assert croppedCT.GetOrigin() == shuffled_roi_image.GetOrigin(), \
#         "Shuffled image origin not same as input image"
#     assert isinstance(shuffled_roi_image, sitk.Image), \
#         "Returned object is not a sitk.Image"
#     assert not np.array_equal(original_pixels, shuffled_roi_pixels), \
#         "No voxel values are being shuffled."
#     assert np.array_equal(np.sort(original_pixels.flatten()),
#                           np.sort(shuffled_roi_pixels.flatten())), \
#         "Shuffled pixel values in ROI are different"
#     assert shuffled_roi_pixels[0,0,0] == -740, \
#         "Voxel outside the ROI is being shuffled. Should just be the ROI voxels."
#     assert shuffled_roi_pixels[7,18,11] == -100, \
#         "Random seed is not working for shuffled ROI image, centre pixel has wrong value. Random seed should be 10."
    

# def test_noROILabel_randomROI(nsclcCropped, randomSeed):
#     " Test passing no roiLabel to makeRandomROI"

#     croppedCT, croppedROI, _ = nsclcCropped

#     randomized_roi_image = makeRandomRoi(croppedCT, croppedROI, randomSeed=randomSeed)
#     original_arr_image = sitk.GetArrayFromImage(croppedCT)
#     minVoxelVal, maxVoxelVal = np.min(original_arr_image), np.max(original_arr_image)

#     randomized_arr_image = sitk.GetArrayFromImage(randomized_roi_image)

#     assert croppedCT.GetSize() == randomized_roi_image.GetSize(), \
#         "Randomized image size not same as input image"
#     assert croppedCT.GetSpacing() == randomized_roi_image.GetSpacing(), \
#         "Randomized image spacing not same as input image"
#     assert croppedCT.GetOrigin() == randomized_roi_image.GetOrigin(), \
#         "Randomized image origin not same as input image"
#     assert isinstance(randomized_roi_image, sitk.Image), \
#         "Returned object is not a sitk.Image"
#     assert not np.array_equal(original_arr_image, randomized_roi_image), \
#         "No voxel values have been changed to random."
#     assert randomized_arr_image.max() <= maxVoxelVal and randomized_arr_image.min() >= minVoxelVal, \
#         "Pixel values are not within the expected range"
#     assert randomized_arr_image[0,0,0] == -740, \
#         "Voxel outside the ROI is being randomized. Should just be the ROI voxels."
#     assert randomized_arr_image[7,18,11] == -400, \
#         "Random seed is not working for randomized ROI image, centre pixel has wrong value. Random seed should be 10."


# def test_noROILabel_randomROIFromDist(nsclcCropped, randomSeed):
#     " Test passing no roiLabel to makeRandomFromRoiDistribution"

#     croppedCT, croppedROI, _ = nsclcCropped

#     randomized_roi_image = makeRandomFromRoiDistribution(croppedCT, croppedROI, randomSeed=randomSeed)
#     original_arr_image = sitk.GetArrayFromImage(croppedCT)

#     randomized_roi_arr_image = sitk.GetArrayFromImage(randomized_roi_image)

#     assert croppedCT.GetSize() == randomized_roi_image.GetSize(), \
#         "Randomized ROI Sampled image size not same as input image"
#     assert croppedCT.GetSpacing() == randomized_roi_image.GetSpacing(), \
#         "Randomized ROI Sampled image spacing not same as input image"
#     assert croppedCT.GetOrigin() == randomized_roi_image.GetOrigin(), \
#         "Randomized ROI Sampled image origin not same as input image"
#     assert isinstance(randomized_roi_image, sitk.Image), \
#         "Returned object is not a sitk.Image"
#     assert not np.array_equal(original_arr_image, randomized_roi_arr_image), \
#         "No voxel values have been changed to random."
#     assert np.all(np.isin(randomized_roi_arr_image.flatten(), original_arr_image.flatten())), \
#         "Retuned object has values not sampled from original image"
#     assert randomized_roi_arr_image[0,0,0] == -740, \
#         "Voxel outside the ROI is being randomized. Should just be the ROI voxels."
#     assert randomized_roi_arr_image[7,18,11] == -5, \
#         "Random seed is not working for randomized from distribution ROI image, centre pixel has wrong value. Random seed should be 10."
    

# def test_noROILabel_shuffleNonROI(nsclcCropped, randomSeed):
#     " Test passing no roiLabel to shuffleNonROI"

#     croppedCT, croppedROI, _ = nsclcCropped

#     shuffled_non_roi_image = shuffleNonROI(croppedCT, croppedROI, randomSeed=randomSeed)

#     original_pixels = sitk.GetArrayFromImage(croppedCT)
#     shuffled_non_roi_pixels = sitk.GetArrayFromImage(shuffled_non_roi_image)

#     assert croppedCT.GetSize() == shuffled_non_roi_image.GetSize(), \
#         "Shuffled image size not same as input image"
#     assert croppedCT.GetSpacing() == shuffled_non_roi_image.GetSpacing(), \
#         "Shuffled image spacing not same as input image"
#     assert croppedCT.GetOrigin() == shuffled_non_roi_image.GetOrigin(), \
#         "Shuffled image origin not same as input image"
#     assert isinstance(shuffled_non_roi_image, sitk.Image), \
#         "Returned object is not a sitk.Image"
#     assert not np.array_equal(original_pixels, shuffled_non_roi_pixels), \
#         "Shuffled image has different pixel values than original image. Should just be original pixels rearranged."
#     assert np.array_equal(np.sort(original_pixels.flatten()),
#                           np.sort(shuffled_non_roi_pixels.flatten())), \
#         "Shuffled pixel values outside ROI are different"
#     assert shuffled_non_roi_pixels[0,0,0] == 54, \
#         "Random seed is not working for shuffled non-ROI image, first voxel has wrong shuffle value. Random seed should be 10."
#     assert shuffled_non_roi_pixels[-1,-1,-1] == -617, \
#         "Random seed is not working for shuffled non-ROI image, last voxel has wrong shuffle value. Random seed should be 10."
#     assert shuffled_non_roi_pixels[7,18,11] == -1, \
#         "ROI is getting shuffled when it shouldn't."
    
    
# def test_noROILabel_randomNonROI(nsclcCropped, randomSeed):
#     " Test passing no roiLabel to makeRandomNonROI"

#     croppedCT, croppedROI, _ = nsclcCropped

#     randomized_non_roi_image = makeRandomNonRoi(croppedCT, croppedROI, randomSeed=randomSeed)

#     original_pixels = sitk.GetArrayFromImage(croppedCT)
#     randomized_non_roi_pixels = sitk.GetArrayFromImage(randomized_non_roi_image)

#     # Make ROI pixels = NaN to help check of min and max values in non-ROI pixels
#     original_roi_pixels = sitk.GetArrayFromImage(croppedROI)
#     roiMask = np.where(original_roi_pixels > 0, np.NaN, 1)
#     masked_randomized_non_roi_pixels = randomized_non_roi_pixels * roiMask
    
#     assert croppedCT.GetSize() == randomized_non_roi_image.GetSize(), \
#         "Randomized image size not same as input image"
#     assert croppedCT.GetSpacing() == randomized_non_roi_image.GetSpacing(), \
#         "Randomized image spacing not same as input image"
#     assert croppedCT.GetOrigin() == randomized_non_roi_image.GetOrigin(), \
#         "Randomized image origin not same as input image"
#     assert isinstance(randomized_non_roi_image, sitk.Image), \
#         "Returned object is not a sitk.Image"
#     assert np.nanmax(masked_randomized_non_roi_pixels) <= np.max(original_pixels) and np.nanmin(masked_randomized_non_roi_pixels) >= np.min(original_pixels), \
#         "Pixel values outside ROI are not within the expected range"
#     assert randomized_non_roi_pixels[0,0,0] == -124, \
#         "Random seed is not working for randomized non-ROI image, first voxel has wrong random value. Random seed should be 10."
#     assert randomized_non_roi_pixels[-1,-1,-1] == 123, \
#         "Random seed is not working for randomized non-ROI image, last voxel has wrong random value. Random seed should be 10."
#     assert randomized_non_roi_pixels[7,18,11] == -1, \
#         "ROI is getting randomized when it shouldn't."
    

# def test_noROILabel_randomNonROIFromDist(nsclcCropped, randomSeed):
#     " Test passing no roiLabel to makeRandomNonRoiFromDistribution"

#     croppedCT, croppedROI, _ = nsclcCropped

#     randomized_non_roi_image = makeRandomNonRoiFromDistribution(croppedCT, croppedROI, randomSeed=randomSeed)

#     original_pixels = sitk.GetArrayFromImage(croppedCT)
#     randomized_non_roi_pixels = sitk.GetArrayFromImage(randomized_non_roi_image)

#     assert croppedCT.GetSize() == randomized_non_roi_image.GetSize(), \
#         "Randomized image size not same as input image"
#     assert croppedCT.GetSpacing() == randomized_non_roi_image.GetSpacing(), \
#         "Randomized image spacing not same as input image"
#     assert croppedCT.GetOrigin() == randomized_non_roi_image.GetOrigin(), \
#         "Randomized image origin not same as input image"
#     assert isinstance(randomized_non_roi_image, sitk.Image), \
#         "Returned object is not a sitk.Image"
#     assert not np.array_equal(original_pixels, randomized_non_roi_pixels), \
#         "No voxel values have been changed to random."
#     assert np.all(np.isin(randomized_non_roi_pixels, original_pixels)), \
#         "Retuned object has values outside ROI not sampled from original image"
#     assert randomized_non_roi_pixels[0,0,0] == -709, \
#         "Random seed is not working for randomized from distribution non-ROI image. Random seed should be 10."
#     assert randomized_non_roi_pixels[-1,-1,-1] == -830, \
#         "Random seed is not working for randomized from distribution non-ROI image. Random seed should be 10."
#     assert randomized_non_roi_pixels[7,18,11] == -1, \
#         "ROI is getting randomized when it shouldn't."