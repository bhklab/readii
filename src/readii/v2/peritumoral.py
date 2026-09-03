#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:36:56 2022
@author: Caryn Geady
"""

'''
PERITUMORAL RADIOMIC FEATURE EXTRACTION

The idea would be to take a series of image and mask path combinations and 
calculate radiomic features for the lesion and the following peritumoral 
regions:
        - lesion core
        - interior rim
        - exterior rim
        - peripheral ring (added 14th March 2023)

Note re. SARC study: images and masks are stored in the 
        '.../OneDrive - UHN/AAA_SARC_LUNG'
folder and are in pairs (images segmented at baseline and after 2 cycles of 
                         chemotherapy).

Ideally, morphological operations can be applied to the masks to generate
temporary arrays to analyze versus storing each mask in memory separately.

'''

# imports
from radiomics import featureextractor
import numpy as np, SimpleITK as sitk
import nrrd, pandas as pd
from skimage.measure import label,regionprops
from skimage.morphology import erosion, dilation, ball
from skimage.transform import rescale


# %% SUPPLEMENTARY FUNCTIONS
''' 
SUPPLEMENTARY FUNCTION : createSubVolumes
This function isolates the sub-volume of the image that we are interested in. 
This way, we can perform operations only on the pixels containing lesion and surrounding pixels (executes faster).
    
    INPUT:
            image         - the original CT volume;
            mask          - the original mask with graduate student-defined ROIs.
            
    OUTPUT:
            image_subV    - image sub-volume, which contains lesion plus surrounding voxels;
            mask_subV     - ground truth labels, which occupies same space the image sub-volumes.
            
'''
def createSubVolumes(image,mask,axial=20,coronal=3):
        
    
    # bounding box of lesion in mask (always 1 per mask image)
    bbox = regionprops(label(msk_V))[0].bbox
    
    # crop a sub-volume corresponding to the ROI (with axial/coronal expansion)
    image_subV = image.copy()
    mask_subV = mask.copy()
    image_subV = image_subV[bbox[0]-axial:bbox[3]+axial,
                            bbox[1]-axial:bbox[4]+axial,
                            bbox[2]-coronal:bbox[-1]+coronal]
    mask_subV = mask_subV[bbox[0]-axial:bbox[3]+axial,
                          bbox[1]-axial:bbox[4]+axial,
                          bbox[2]-coronal:bbox[-1]+coronal]
    
    return image_subV,mask_subV

''' 
SUPPLEMENTARY FUNCTION : resampleVolumes
This function resamples the sub-volume and corresponding mask to isotropic voxel size (1mm, 1mm, 1mm). 
    
    INPUT:
            image     - the CT sub-volume;
            mask      - the mask occupying the same space as the image_subV;
            meta      - dictionary with original image and/or mask metadata (they are the same so either dictionary works).
            
    OUTPUT:
            img_RS    - the resampled CT sub-volume;
            msk_RS    - the resampled mask occupying the same space as the resampled CT sub-volume.
                     
'''
def resampleVolumes(image,mask,meta):

    dims = np.diagonal(meta['space directions'])

    scaleFac = []
            
    for d in dims:
        if d < 1:
            scaleFac.append(1/float(d))
        else:
            scaleFac.append(float(d))
 
    # note the logical expression for the mask b/c the output from rescale is not binary
    msk_RS = 1 * (rescale(mask, scale = (scaleFac[0],scaleFac[1],scaleFac[2]), preserve_range = True, anti_aliasing=None) > 0.25)
    img_RS = rescale(image, scale = (scaleFac[0],scaleFac[1],scaleFac[2]), preserve_range = True, anti_aliasing=True)
            
    return img_RS,msk_RS

''' 
SUPPLEMENTARY FUNCTIONS : morphOps
This function isolates sub-regions of the segmented lesion (core, periphery, etc.) and calculates statistics of interest. 

    INPUT:
            mask      - the resampled mask occupying the same space as the img_sub;
            region    - peritumoral region  of interest 
            r         - optional argument (specified to 2mm, which is appropriate for the resampled sub-volume).
            
    OUTPUT:
            morphMsk  - mask for peritumoral region of interest
                     
'''

def morphOps(mask,region='whole lesion',r=2):
    
    mask = mask == 1
            
    if region == 'whole lesion':
        morphMsk = 1 * mask
    
    if region == 'lesion core':
        morphMsk = 1 * erosion(mask,ball(radius = r))

    if region == 'interior rim':
        morphMsk = 1 * np.logical_and(mask,~erosion(mask,ball(radius = r)))
        
    if region == 'exterior rim':
        morphMsk = 1 * np.logical_and(~mask,dilation(mask,ball(radius = r)))
        
    if region == 'peripheral ring':
        morphMsk = 1 * np.logical_and(~erosion(mask,ball(radius = r)),dilation(mask,ball(radius = r)))   
        
    return morphMsk

# %%

'''
ANALYSIS STEPS:
    - load image and mask(s)
    - create a sub-volume around the mask (hopefully should speed things up)
    - resample both to uniform spacing
    - morphological operations (omit for now)
    - convert to SITK image
    - extract features from each region
    - combine into unified .csv data table output
    
'''

# file containing paths to images and masks -- 1 row == 1 lesion (most patients have >1 lesion so repeat images exist)
dat = pd.read_csv('/Users/EL-CAPITAN-2016/Documents/Python/pyradiomics/lung_lesion_pyrad_2022.csv')
idList = dat.ID         # series of patient IDs
studyList = dat.Study   # series of study time (ie, baseline or cycle 2)
locList = dat.Info      # series of lesion locations 
imgList = dat.Image     # series of paths to images
mskList = dat.Mask      # series of paths to masks

morphs = ['whole lesion','lesion core','interior rim','exterior rim','peripheral ring']

patientID = []          # patient ID
study = []              # baseline or cycle2
location = []           # where in the lung, from grad contour
morphRegion = []        # omit for now
imageFiles = []         # image file path
maskFiles = []          # mask file path

errorLog = []
radiomics = pd.DataFrame(data=None)
# instantiate the extractor (pyradiomics)
params = '/Users/EL-CAPITAN-2016/Documents/Python/pyradiomics/examples/exampleSettings/exampleCT.yaml'
extractor = featureextractor.RadiomicsFeatureExtractor(params)


for i in range(len(imgList)):  # len(imgList)
    
    print('Loading image -- {:1f}% complete!'.format((i+1)/len(imgList)*100))
    # read image and corresponding mask
    img_V,img_d = nrrd.read(imgList[i])
    msk_V,msk_d = nrrd.read(mskList[i])
    
    # calculate voxel volume
    msk_voxel_volume = np.product(np.diagonal(msk_d['space directions']))   # in mm^3
    img_voxel_volume = np.product(np.diagonal(img_d['space directions']))   # in mm^3
        
    # if the image and mask do not have the same voxel volume, do not process
    if abs(msk_voxel_volume - img_voxel_volume) > 1e-4:
        print('ERROR, {}: image and mask must have same voxel volumes'.format(imgList[i]))
        errorLog.append(['geo mismatch',imgList[i],mskList[i],abs(msk_voxel_volume - img_voxel_volume)])
        continue
    
    # create a sub-volume around the mask (faster processing)
    img_sub,msk_sub = createSubVolumes(img_V,msk_V)
    
    # resample to uniform spacing (1mm,1mm,1mm)
    img_RS,msk_RS = resampleVolumes(img_sub,msk_sub,img_d)
    
    for j in range(len(morphs)):  # len(morphs)
        # ---------- IMAGE OPERATIONS ----------
        morphMask = morphOps(msk_RS,region=morphs[j])
        if np.sum(morphMask) < 64:
            errorLog.append(['mask size',imgList[i],mskList[i],morphs[j]])
            continue
        # convert to SITK object for radiomic feature extraction
        image = sitk.GetImageFromArray(img_RS)
        mask = sitk.GetImageFromArray(morphMask)
        
        # extract features and convert to dataframe object
        features = pd.DataFrame.from_dict(extractor.execute(image,mask), 
                                          orient='index').transpose()   
        # concatenate
        radiomics = pd.concat([radiomics, features], ignore_index=True)
        
        # ---------- HEADER OPERATIONS ----------
        patientID.append(idList.iloc[i])
        study.append(studyList.iloc[i])
        location.append(locList.iloc[i])
        morphRegion.append(morphs[j])
        imageFiles.append(imgList.iloc[i])
        maskFiles.append(mskList.iloc[i])
        
header = pd.DataFrame(list(zip(patientID,study,location,morphRegion,imageFiles,maskFiles)),
                      columns =['ID','Study','Location','MorphRegion','Image','Mask'])

result = pd.concat([header,radiomics],axis=1)    
del(patientID,study,location,morphRegion,imageFiles,maskFiles)