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

    segBoundingBox, correctedROIImage = imageoperations.checkMask(nsclcCTImage, alignedROIImage,
                                                                  label=segmentationLabel)

    if correctedROIImage is not None:
        alignedROIImage = correctedROIImage

    croppedCT, croppedROI = imageoperations.cropToTumorMask(nsclcCTImage, alignedROIImage, segBoundingBox)

    return croppedCT, croppedROI, segmentationLabel

@pytest.fixture()
def randomSeed():
    return 10

def test_shuffleImage(nsclcCTImage, randomSeed):
    " Test negative control to shuffle the whole image"

    shuffled_image = shuffleImage(nsclcCTImage, randomSeed)
    original_pixels = sitk.GetArrayFromImage(nsclcCTImage).flatten()
    shuffled_pixels = sitk.GetArrayFromImage(shuffled_image).flatten()

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
    assert np.array_equal(np.sort(original_pixels),
                          np.sort(shuffled_pixels)), \
        "Shuffled image has different pixel values"
    assert shuffled_pixels[0,0,0] == -987, \
        "Random seed is not working for shuffled image. Random seed should be 10."
    assert shuffled_pixels[-1,-1,-1] == 10, \
        "Random seed is not working for shuffled image. Random seed should be 10."


def test_makeRandomImage(nsclcCTImage):
    " Test negative control to randomize the pixels of the whole image"

    randomized_image = makeRandomImage(nsclcCTImage)
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

    for _ in range(5):
        size = nsclcCTImage.GetSize()
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        assert randomized_image.GetPixel(x, y, z) != nsclcCTImage.GetPixel(x, y, z), \
            "Random pixel value not shuffled"


def test_shuffleROI(nsclcCropped):
    " Test negative control to shuffle the roi of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    shuffled_image = shuffleROI(croppedCT, croppedROI, segmentationLabel)

    original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedROI.GetSize()[0]) for y in
                       range(croppedROI.GetSize()[1]) for z in range(croppedROI.GetSize()[2]) if
                       croppedROI.GetPixel(x, y, z) == segmentationLabel]

    shuffled_pixels = [shuffled_image.GetPixel(x, y, z) for x in range(croppedROI.GetSize()[0]) for y in
                       range(croppedROI.GetSize()[1]) for z in range(croppedROI.GetSize()[2]) if
                       croppedROI.GetPixel(x, y, z) == segmentationLabel]

    assert croppedCT.GetSize() == shuffled_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert croppedCT.GetSpacing() == shuffled_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert croppedCT.GetOrigin() == shuffled_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_pixels), \
        "Pixel values in ROI are not shuffled"
    assert np.array_equal(np.sort(original_pixels),
                          np.sort(shuffled_pixels)), \
        "Shuffled pixel values in ROI are different"


def test_makeRandomRoi(nsclcCropped):
    " Test negative control to randomize the pixels of the ROI of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_image = makeRandomRoi(croppedCT, croppedROI, segmentationLabel)
    original_arr_image = sitk.GetArrayFromImage(croppedCT)
    minVoxelVal, maxVoxelVal = np.min(original_arr_image), np.max(original_arr_image)

    randomized_arr_image = sitk.GetArrayFromImage(randomized_image)

    assert croppedCT.GetSize() == randomized_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert randomized_arr_image.max() <= maxVoxelVal and randomized_arr_image.min() >= minVoxelVal, \
        "Pixel values are not within the expected range"

    size = croppedROI.GetSize()
    for _ in range(5):
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        if croppedROI.GetPixel(x, y, z) == segmentationLabel:
            assert randomized_image.GetPixel(x, y, z) != croppedCT.GetPixel(x, y, z), \
                "Pixel value not randomized"


def test_shuffleNonROI(nsclcCropped):
    " Test negative control to shuffle the pixels outside roi of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    shuffled_image = shuffleNonROI(croppedCT, croppedROI, segmentationLabel)

    original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
                       for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
                       if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
                                                                                                             z) != segmentationLabel]

    shuffled_pixels = [shuffled_image.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
                       for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
                       if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
                                                                                                             z) != segmentationLabel]
    assert croppedCT.GetSize() == shuffled_image.GetSize(), \
        "Shuffled image size not same as input image"
    assert croppedCT.GetSpacing() == shuffled_image.GetSpacing(), \
        "Shuffled image spacing not same as input image"
    assert croppedCT.GetOrigin() == shuffled_image.GetOrigin(), \
        "Shuffled image origin not same as input image"
    assert isinstance(shuffled_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert not np.array_equal(original_pixels, shuffled_pixels), \
        "Pixel values outside ROI are not shuffled"
    assert np.array_equal(np.sort(original_pixels),
                          np.sort(shuffled_pixels)), \
        "Shuffled pixel values outside ROI are different"

    for x in range(croppedROI.GetSize()[0]):
        for y in range(croppedROI.GetSize()[1]):
            for z in range(croppedROI.GetSize()[2]):
                if croppedROI.GetPixel(x, y, z) == segmentationLabel:
                    assert croppedCT.GetPixel(x, y, z) == shuffled_image.GetPixel(x, y, z), \
                        "Pixel values within ROI have changed"


def test_makeRandomNonRoi(nsclcCropped):
    " Test negative control to randomize the pixels outside the ROI of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_image = makeRandomNonRoi(croppedCT, croppedROI, segmentationLabel)

    original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
                       for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
                       if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
                                                                                                             z) != segmentationLabel]

    randomized_pixels = [randomized_image.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
                         for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
                         if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
                                                                                                               z) != segmentationLabel]

    assert croppedCT.GetSize() == randomized_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert max(randomized_pixels) <= max(original_pixels) and min(randomized_pixels) >= min(original_pixels), \
        "Pixel values outside ROI are not within the expected range"

    for x in range(croppedROI.GetSize()[0]):
        for y in range(croppedROI.GetSize()[1]):
            for z in range(croppedROI.GetSize()[2]):
                if croppedROI.GetPixel(x, y, z) == segmentationLabel:
                    assert croppedCT.GetPixel(x, y, z) == randomized_image.GetPixel(x, y, z), \
                        "Pixel values within ROI have changed"


def test_randomizeImageFromDistribtutionSampling(nsclcCTImage):
    " Test negative control to uniformly sample the pixels of the whole image from the images pixel distribution"

    randomized_sampled_image = randomizeImageFromDistribtutionSampling(nsclcCTImage)
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

    for _ in range(5):
        size = nsclcCTImage.GetSize()
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        assert randomized_sampled_image.GetPixel(x, y, z) in flattened_randomized_arr_image, \
            "Random pixel value not sampled correctly"


def test_makeRandomFromRoiDistribution(nsclcCropped):
    " Test negative control to uniformly sample the pixels of the ROI of the image randomly"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_image = makeRandomFromRoiDistribution(croppedCT, croppedROI, segmentationLabel)
    original_arr_image = sitk.GetArrayFromImage(croppedCT)
    flatten_org_arr_image = original_arr_image.flatten()

    randomized_arr_image = sitk.GetArrayFromImage(randomized_image)
    flattened_randomized_arr_image = randomized_arr_image.flatten()

    assert croppedCT.GetSize() == randomized_image.GetSize(), \
        "Randomized ROI Sampled image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_image.GetSpacing(), \
        "Randomized ROI Sampled image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_image.GetOrigin(), \
        "Randomized ROI Sampled image origin not same as input image"
    assert isinstance(randomized_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert np.all(np.isin(flattened_randomized_arr_image, flatten_org_arr_image)), \
        "Retuned object has values not sampled from original image"

    size = croppedROI.GetSize()
    for _ in range(5):
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        z = random.randint(0, size[2] - 1)
        if croppedROI.GetPixel(x, y, z) == segmentationLabel:
            assert randomized_image.GetPixel(x, y, z) in flatten_org_arr_image, \
                "Pixel value not sampled correctly"

def test_makeRandomNonRoiFromDistribution(nsclcCropped):
    " Test negative control to randomize the pixels outside the ROI of the image"

    croppedCT, croppedROI, segmentationLabel = nsclcCropped

    randomized_image = makeRandomNonRoiFromDistribution(croppedCT, croppedROI, segmentationLabel)

    original_pixels = [croppedCT.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
                       for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
                       if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
                                                                                                             z) != segmentationLabel]

    randomized_pixels = [randomized_image.GetPixel(x, y, z) for x in range(croppedCT.GetSize()[0]) \
                         for y in range(croppedCT.GetSize()[1]) for z in range(croppedCT.GetSize()[2]) \
                         if x > croppedROI[0] or y > croppedROI[1] or z > croppedROI[2] or croppedROI.GetPixel(x, y,
                                                                                                               z) != segmentationLabel]

    assert croppedCT.GetSize() == randomized_image.GetSize(), \
        "Randomized image size not same as input image"
    assert croppedCT.GetSpacing() == randomized_image.GetSpacing(), \
        "Randomized image spacing not same as input image"
    assert croppedCT.GetOrigin() == randomized_image.GetOrigin(), \
        "Randomized image origin not same as input image"
    assert isinstance(randomized_image, sitk.Image), \
        "Returned object is not a sitk.Image"
    assert np.all(np.isin(randomized_pixels, original_pixels)), \
        "Retuned object has values outside ROI not sampled from original image"

    for x in range(croppedROI.GetSize()[0]):
        for y in range(croppedROI.GetSize()[1]):
            for z in range(croppedROI.GetSize()[2]):
                if croppedROI.GetPixel(x, y, z) == segmentationLabel:
                    assert croppedCT.GetPixel(x, y, z) == randomized_image.GetPixel(x, y, z), \
                        "Pixel values within ROI have changed"