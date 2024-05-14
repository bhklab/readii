import numpy as np

from readii.negative_controls import *
from readii.image_processing import *
from radiomics import imageoperations

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

def test_shuffleImage(nsclcCTImage, randomSeed):
    " Test negative control to shuffle the whole image"

    shuffled_image = shuffleImage(nsclcCTImage, randomSeed)
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
    # assert np.array_equal(np.sort(original_pixels),
    #                       np.sort(shuffled_pixels)), \
    #     "Shuffled image has different pixel values"
    assert shuffled_pixels[0,0,0] == -987, \
        "Random seed is not working for shuffled image. Random seed should be 10."
    assert shuffled_pixels[-1,-1,-1] == 10, \
        "Random seed is not working for shuffled image. Random seed should be 10."


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
        "Random seed is not working for random image. Random seed should be 10."
    assert randomized_arr_image[-1,-1,-1] == 90, \
        "Random seed is not working for random image. Random seed should be 10."

    for _ in range(5):
        size = nsclcCTImage.GetSize()
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        assert randomized_image.GetPixel(x, y, z) != nsclcCTImage.GetPixel(x, y, z), \
            "Random pixel value not shuffled"


def test_shuffleROI(nsclcCropped, randomSeed):
    " Test negative control to shuffle the roi of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    shuffled_roi_image = shuffleROI(croppedCT, croppedROI, segmentationLabel, randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    shuffled_roi_pixels = sitk.GetArrayFromImage(shuffled_roi_image)

    # original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedROI.GetSize()[0]) for y in
    #                    range(croppedROI.GetSize()[1]) for z in range(croppedROI.GetSize()[2]) if
    #                    croppedROI.GetPixel(x, y, z) == segmentationLabel]

    # shuffled_pixels = [shuffled_roi_image.GetPixel(x, y, z) for x in range(croppedROI.GetSize()[0]) for y in
    #                    range(croppedROI.GetSize()[1]) for z in range(croppedROI.GetSize()[2]) if
    #                    croppedROI.GetPixel(x, y, z) == segmentationLabel]

    assert croppedCT.GetSize() == shuffled_roi_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert croppedCT.GetSpacing() == shuffled_roi_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert croppedCT.GetOrigin() == shuffled_roi_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_roi_pixels), \
        "Pixel values in ROI are not shuffled"
    # assert np.array_equal(np.sort(original_pixels),
    #                       np.sort(shuffled_pixels)), \
    #     "Shuffled pixel values in ROI are different"
    assert shuffled_roi_pixels[0,0,0] == -740, \
        "Voxel outside the ROI is being shuffled. Should just be the ROI voxels."
    assert shuffled_roi_pixels[7,18,11] == -100, \
        "Random seed is not working for shuffled ROI image, centre pixel has wrong value. Random seed should be 10."


def test_makeRandomRoi(nsclcCropped, randomSeed):
    " Test negative control to randomize the pixels of the ROI of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_roi_image = makeRandomRoi(croppedCT, croppedROI, segmentationLabel, randomSeed)
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
    assert randomized_arr_image.max() <= maxVoxelVal and randomized_arr_image.min() >= minVoxelVal, \
        "Pixel values are not within the expected range"
    assert randomized_arr_image[0,0,0] == -740, \
        "Voxel outside the ROI is being randomized. Should just be the ROI voxels."
    assert randomized_arr_image[7,18,11] == -400, \
        "Random seed is not working for randomized ROI image, centre pixel has wrong value. Random seed should be 10."

    size = croppedROI.GetSize()
    for _ in range(5):
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        if croppedROI.GetPixel(x, y, z) == segmentationLabel:
            assert randomized_roi_image.GetPixel(x, y, z) != croppedCT.GetPixel(x, y, z), \
                "Pixel value not randomized"


def test_shuffleNonROI(nsclcCropped, randomSeed):
    " Test negative control to shuffle the pixels outside roi of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    shuffled_non_roi_image = shuffleNonROI(croppedCT, croppedROI, segmentationLabel, randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    shuffled_non_roi_pixels = sitk.GetArrayFromImage(shuffled_non_roi_image)

    # original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
    #                    for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
    #                    if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
    #                                                                                                          z) != segmentationLabel]

    # shuffled_pixels = [shuffled_non_roi_image.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
    #                    for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
    #                    if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
    #                                                                                                          z) != segmentationLabel]
    assert croppedCT.GetSize() == shuffled_non_roi_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert croppedCT.GetSpacing() == shuffled_non_roi_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert croppedCT.GetOrigin() == shuffled_non_roi_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_non_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_non_roi_pixels), \
        "Pixel values outside ROI are not shuffled"
    # assert np.array_equal(np.sort(original_pixels),
    #                       np.sort(shuffled_non_roi_pixels)), \
    #     "Shuffled pixel values outside ROI are different"
    assert shuffled_non_roi_pixels[0,0,0] == 54, \
        "Random seed is not working for shuffled non-ROI image. Random seed should be 10."
    assert shuffled_non_roi_pixels[-1,-1,-1] == -617, \
        "Random seed is not working for shuffled non-ROI image. Random seed should be 10."
    assert shuffled_non_roi_pixels[7,18,11] == -1, \
        "ROI is getting shuffled when it shouldn't."

    for x in range(croppedROI.GetSize()[0]):
        for y in range(croppedROI.GetSize()[1]):
            for z in range(croppedROI.GetSize()[2]):
                if croppedROI.GetPixel(x, y, z) == segmentationLabel:
                    assert croppedCT.GetPixel(x, y, z) == shuffled_non_roi_image.GetPixel(x, y, z), \
                        "Pixel values within ROI have changed"


def test_makeRandomNonRoi(nsclcCropped, randomSeed):
    " Test negative control to randomize the pixels outside the ROI of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_non_roi_image = makeRandomNonRoi(croppedCT, croppedROI, segmentationLabel, randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    randomized_non_roi_pixels = sitk.GetArrayFromImage(randomized_non_roi_image)

    # original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
    #                    for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
    #                    if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
    #                                                                                                          z) != segmentationLabel]

    # randomized_pixels = [randomized_non_roi_image.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
    #                      for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
    #                      if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
    #                                                                                                            z) != segmentationLabel]

    assert croppedCT.GetSize() == randomized_non_roi_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_non_roi_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_non_roi_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_non_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    # assert max(randomized_non_roi_pixels) <= max(original_pixels) and min(randomized_non_roi_pixels) >= min(original_pixels), \
    #     "Pixel values outside ROI are not within the expected range"
    assert randomized_non_roi_pixels[0,0,0] == -124, \
        "Random seed is not working for randomized non-ROI image. Random seed should be 10."
    assert randomized_non_roi_pixels[-1,-1,-1] == 123, \
        "Random seed is not working for randomized non-ROI image. Random seed should be 10."
    assert randomized_non_roi_pixels[7,18,11] == -1, \
        "ROI is getting randomized when it shouldn't."

    for x in range(croppedROI.GetSize()[0]):
        for y in range(croppedROI.GetSize()[1]):
            for z in range(croppedROI.GetSize()[2]):
                if croppedROI.GetPixel(x, y, z) == segmentationLabel:
                    assert croppedCT.GetPixel(x, y, z) == randomized_non_roi_image.GetPixel(x, y, z), \
                        "Pixel values within ROI have changed"


def test_randomizeImageFromDistributionSampling(nsclcCTImage, randomSeed):
    " Test negative control to uniformly sample the pixels of the whole image from the images pixel distribution"

    randomized_sampled_image = randomizeImageFromDistributionSampling(nsclcCTImage, randomSeed)
    original_arr_image = sitk.GetArrayFromImage(nsclcCTImage)
    flatten_org_arr_image = original_arr_image.flatten()

    randomized_arr_image = sitk.GetArrayFromImage(randomized_sampled_image)
    flattened_randomized_arr_image = randomized_arr_image.flatten()

    assert nsclcCTImage.GetSize() == randomized_sampled_image.GetSize(), \
        "Randomized sampled image size not same as input image"
    assert nsclcCTImage.GetSpacing() == randomized_sampled_image.GetSpacing(), \
        "Randomized sampled image spacing not same as input image"
    assert nsclcCTImage.GetOrigin() == randomized_sampled_image.GetOrigin(), \
        "Randomized sampled image origin not same as input image"
    assert isinstance(randomized_sampled_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert np.all(np.isin(flattened_randomized_arr_image, flatten_org_arr_image)), \
        "Retuned object has values not sampled from original image"
    assert randomized_arr_image[0,0,0] == -1005, \
        "Random seed is not working for randomized from distribution image. Random seed should be 10."
    assert randomized_arr_image[-1,-1,-1] == 414, \
        "Random seed is not working for randomized from distribution image. Random seed should be 10."

    for _ in range(5):
        size = nsclcCTImage.GetSize()
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        assert randomized_sampled_image.GetPixel(x, y, z) in flattened_randomized_arr_image, \
            "Random pixel value not sampled correctly"


def test_makeRandomFromRoiDistribution(nsclcCropped, randomSeed):
    " Test negative control to uniformly sample the pixels of the ROI of the image randomly"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_roi_image = makeRandomFromRoiDistribution(croppedCT, croppedROI, segmentationLabel, randomSeed)
    original_arr_image = sitk.GetArrayFromImage(croppedCT)
    flatten_org_arr_image = original_arr_image.flatten()

    randomized_roi_arr_image = sitk.GetArrayFromImage(randomized_roi_image)
    flattened_randomized_roi_arr_image = randomized_roi_arr_image.flatten()

    assert croppedCT.GetSize() == randomized_roi_image.GetSize(), \
        "Randomized ROI Sampled image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_roi_image.GetSpacing(), \
        "Randomized ROI Sampled image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_roi_image.GetOrigin(), \
        "Randomized ROI Sampled image origin not same as input image"
    assert isinstance(randomized_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert np.all(np.isin(flattened_randomized_roi_arr_image, flatten_org_arr_image)), \
        "Retuned object has values not sampled from original image"
    assert randomized_roi_arr_image[0,0,0] == -740, \
        "Voxel outside the ROI is being randomized. Should just be the ROI voxels."
    assert randomized_roi_arr_image[7,18,11] == -5, \
        "Random seed is not working for randomized from distribution ROI image, centre pixel has wrong value. Random seed should be 10."

    size = croppedROI.GetSize()
    for _ in range(5):
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        if croppedROI.GetPixel(x, y, z) == segmentationLabel:
            assert randomized_roi_image.GetPixel(x, y, z) in flatten_org_arr_image, \
                "Pixel value not sampled correctly"


def test_makeRandomNonRoiFromDistribution(nsclcCropped, randomSeed):
    " Test negative control to randomize the pixels outside the ROI of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_non_roi_image = makeRandomNonRoiFromDistribution(croppedCT, croppedROI, segmentationLabel, randomSeed)

    original_pixels = sitk.GetArrayFromImage(croppedCT)
    randomized_non_roi_pixels = sitk.GetArrayFromImage(randomized_non_roi_image)

    # original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
    #                    for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
    #                    if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
    #                                                                                                          z) != segmentationLabel]

    # randomized_non_roi_pixels = [randomized_non_roi_image.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
    #                      for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
    #                      if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
    #                                                                                                            z) != segmentationLabel]

    assert croppedCT.GetSize() == randomized_non_roi_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_non_roi_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_non_roi_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_non_roi_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert np.all(np.isin(randomized_non_roi_pixels, original_pixels)), \
        "Retuned object has values outside ROI not sampled from original image"
    assert randomized_non_roi_pixels[0,0,0] == -709, \
        "Random seed is not working for randomized from distribution non-ROI image. Random seed should be 10."
    assert randomized_non_roi_pixels[-1,-1,-1] == -830, \
        "Random seed is not working for randomized from distribution non-ROI image. Random seed should be 10."
    assert randomized_non_roi_pixels[7,18,11] == -1, \
        "ROI is getting randomized when it shouldn't."

    for x in range(croppedROI.GetSize()[0]):
        for y in range(croppedROI.GetSize()[1]):
            for z in range(croppedROI.GetSize()[2]):
                if croppedROI.GetPixel(x, y, z) == segmentationLabel:
                    assert croppedCT.GetPixel(x, y, z) == randomized_non_roi_image.GetPixel(x, y, z), \
                        "Pixel values within ROI have changed"