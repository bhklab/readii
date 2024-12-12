# READII
<!--intro-start-->
[![codecov](https://codecov.io/gh/bhklab/readii/graph/badge.svg?token=obsN5dhXPx)](https://codecov.io/gh/bhklab/readii)
[![CI-CD](https://github.com/bhklab/readii/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/bhklab/readii/actions/workflows/ci-cd.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/bhklab/readii/badge)](https://www.codefactor.io/repository/github/bhklab/readii)

![GitHub Release](https://img.shields.io/github/v/release/bhklab/readii)
[![pixi-badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json&style=flat-square)](https://github.com/prefix-dev/pixi)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/readii)](https://pypi.org/project/readii/)
[![PyPI - Version](https://img.shields.io/pypi/v/readii)](https://pypi.org/project/readii/)
[![PyPI - Format](https://img.shields.io/pypi/format/readii)](https://pypi.org/project/readii/)
[![Downloads](https://static.pepy.tech/badge/readii)](https://pepy.tech/project/readii)
[![Docker Pulls](https://img.shields.io/docker/pulls/bhklab/readii)](https://hub.docker.com/r/bhklab/readii)

**R**adiomic **E**xtraction and **A**nalysis for **DI**COM **I**mages

A package to extract radiomic features from DICOM CT images.

## Installation

```bash
$ pip install readii
```

### (recommended) Create new `pixi` environment for a project

```bash
mkdir my_project
cd my_project
pixi init
pixi add --pypi readii
```

### (recommended) Create new conda virtual environment

```bash
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

Please use the following angular commit message format:

```text
<type>(optional scope): short summary in present tense

(optional body: explains motivation for the change)

(optional footer: note BREAKING CHANGES here, and issues to be closed)

```

`<type>` refers to the kind of change made and is usually one of:

- `feat`: A new feature.
- `fix`: A bug fix.
- `docs`: Documentation changes.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Changes to the test framework.
- `build`: Changes to the build process or tools.

`scope` is an optional keyword that provides context for where the change was made. It can be anything relevant to your package or development workflow (e.g., it could be the module or function - name affected by the change).

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

### Serve Documentation Locally

```bash
pixi run -e docs doc-serve
```

## License

`readii` was created by Katy Scott. It is licensed under the terms of the MIT license.

<!--intro-end-->