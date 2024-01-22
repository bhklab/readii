# YAREA

Yet Another Radiomic Extraction and Analysis pipeline

A package to extract radiomic features from DICOM CT images.

## Installation

```bash
$ pip install yarea
```

### (recommended) Create new conda virtual environment
```
conda create -n yarea python=3.9
conda activate yarea
pip install yarea
```

## Usage
`yarea` is a tool to perform radiomic feature extraction on DICOM CT images with region of interest (ROI) segmentations as either DICOM SEG or RTSTRUCT.

```bash
$ yarea [INPUT DIRECTORY] [OUTPUT DIRECTORY] \
  --roi_names [str] \
  --pyradiomics_setting [str] \
  --negative_controls [str: randomized_full,randomized_roi,randomized_non_roi,shuffled_full,shuffled_roi,shuffled_non_roi] \
  --parallel [flag]
  --update [flag]
```


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`yarea` was created by Katy Scott. It is licensed under the terms of the MIT license.

## Credits

`yarea` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
