# READII
[![Docker Pulls](https://img.shields.io/docker/pulls/bhklab/readii)](https://hub.docker.com/r/bhklab/readii)

![GitHub Release](https://img.shields.io/github/v/release/bhklab/readii)


**R**adiomic **E**xtraction and **A**nalysis for **DI**COM **I**mages

A package to extract radiomic features from DICOM CT images.

## Installation

```bash
$ pip install readii
```

### (recommended) Create new conda virtual environment
```
conda create -n readii python=3.9
conda activate readii
pip install readii
```

## Usage
`readii` is a tool to perform radiomic feature extraction on DICOM CT images with region of interest (ROI) segmentations as either DICOM SEG or RTSTRUCT.

```bash
$ readii [INPUT DIRECTORY] [OUTPUT DIRECTORY] \
  --roi_names [str] \
  --pyradiomics_setting [str] \
  --negative_controls [str: shuffled_full,shuffled_roi,shuffled_non_roi,randomized_full,randomized_roi,randomized_non_roi,randomized_sampled_full,randomized_sampled_roi, randomized_sampled_non_roi] \
  --parallel [flag]
  --update [flag]
```

### Negative control options

Negative controls are applied to one of three masks: 
1. full = voxels in the entire image
2. roi = just voxels within the specified region of interest (ROI) in the segmentation
3. non_roi = all voxels except the ROI.

The three transformations are:
1. shuffle = shuffle all voxels in the specified mask
2. randomized = randomly generate new values within the original range within the specified mask
3. randomized_sampled = randomly sample original values with replacement to get new values within the specified mask


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`readii` was created by Katy Scott. It is licensed under the terms of the MIT license.

## Credits

`readii` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
