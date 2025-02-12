# CHANGELOG


## v1.35.0 (2025-02-12)

### Features

- Add image cropping preprocessing ([#119](https://github.com/bhklab/readii/pull/119),
  [`978bdb5`](https://github.com/bhklab/readii/commit/978bdb51bf6669b95a02ce2a94ff8c4fc3735169))

Using crop methods from med-imagetools, setup three crop methods that can be used as preprocessing
  steps for feature extraction. Three methods migrated from readii-fmcib = bbox, centroid, cube

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Refined visualization in the notebook with updated image display settings,
  including adjusted colormaps and layout. - Introduced functionality to crop and resize images and
  masks using multiple methods and configurable dimensions. - **Enhancements** - Improved image
  slice display with the option to specify a custom display axis. - **Tests** - Added comprehensive
  tests to validate the new image processing and cropping features. - **Documentation** 	- Updated
  notebook metadata and display settings. <!-- end of auto-generated comment: release notes by
  coderabbit.ai -->

---------

Co-authored-by: Jermiah <jermiahjoseph98@gmail.com>

### Refactoring

- Remove io module allowance, wrong branch
  ([`3a4e9d0`](https://github.com/bhklab/readii/commit/3a4e9d0993eb7c8e8846e9795990e12155fcde16))

- Update ruff to allow io module
  ([`efd5a32`](https://github.com/bhklab/readii/commit/efd5a32beab1f75aa469eed872542c69737aa5be))


## v1.34.3 (2025-01-30)

### Bug Fixes

- Pattern resolver update ([#116](https://github.com/bhklab/readii/pull/116),
  [`39a6d6b`](https://github.com/bhklab/readii/commit/39a6d6b12092dd78e7e237221d0531f4d3f47306))

`PatternResolver` in `med-imagetools` updated the input argument from `pattern_parser` to
  `pattern_matcher`, updated this to match here.

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **Chores** - Updated parameter naming in the `PatternResolver` class for improved clarity and
  consistency. - Modified the `roiNames` parameter format in segmentation loading tests for better
  structure and clarity. - Adjusted expected output labels in segmentation tests to reflect new
  naming conventions. - Reorganized import statements to source functions from a new module,
  maintaining accessibility. <!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.34.2 (2025-01-30)

### Bug Fixes

- Axes labelling in plotCrossCorrHeatmap ([#115](https://github.com/bhklab/readii/pull/115),
  [`49b38ce`](https://github.com/bhklab/readii/commit/49b38ce8096ed9be0ab49eac4e9dfe06f6ad87f5))

Swap vertical and horizontal feature labels on x and y axes of cross correlation heatmap

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- **Bug Fixes** - Corrected axis label assignments in cross-correlation heatmap visualization to
  improve accuracy of feature representation.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.34.1 (2025-01-15)

### Bug Fixes

- Update toml to fix deprecated "depends_on" key ([#109](https://github.com/bhklab/readii/pull/109),
  [`2c2c324`](https://github.com/bhklab/readii/commit/2c2c324ce3338267aa6d04fc538771cbe0414a07))


## v1.34.0 (2024-12-31)

### Features

- Add overwrite variable to plot self and cross corr functions
  ([#108](https://github.com/bhklab/readii/pull/108),
  [`d1f9853`](https://github.com/bhklab/readii/commit/d1f9853cf4613762ccb0f0885e77db4cb07eb71b))

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- **New Features** - Added an optional `overwrite` parameter to correlation plotting functions -
  Enhanced control over file saving behavior when generating correlation plots 	- Users can now
  choose whether to replace existing plot files

<!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.33.0 (2024-12-30)

### Features

- Add error for when file output by CorrelationWriter already exists
  ([#106](https://github.com/bhklab/readii/pull/106),
  [`ef58923`](https://github.com/bhklab/readii/commit/ef589237be7dd41769be507a24e0a406dcdc603e))

Makes it easier to catch times when file exists without resolving the path twice

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- **New Features** - Added a new, more specific exception for handling file existence scenarios
  during correlation writing.

- **Documentation** 	- Updated method documentation to reflect new error handling behavior.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.32.0 (2024-12-30)

### Features

- Update plot correlation functions ([#104](https://github.com/bhklab/readii/pull/104),
  [`9baffe9`](https://github.com/bhklab/readii/commit/9baffe93e6d3bb9f67887d98348dece5a4de69cf))

add self and cross correlation plot functions

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Introduced functionality for plotting self and cross correlation heatmaps and
  histograms. - Added methods for generating histograms with customizable parameters and optional
  saving options. - **Bug Fixes** - Enhanced error handling for plot saving to prevent overwriting
  existing files. - **Tests** - Added a comprehensive suite of unit tests for correlation plotting
  functionalities, ensuring correct outputs and file handling. <!-- end of auto-generated comment:
  release notes by coderabbit.ai -->


## v1.31.0 (2024-12-19)

### Features

- Update correlation functions to get subsections of matrix
  ([#103](https://github.com/bhklab/readii/pull/103),
  [`343d876`](https://github.com/bhklab/readii/commit/343d876272d3e34592b46ba37586f4bcf7cf54f8))

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Enhanced correlation analysis methods for improved clarity and functionality. -
  Introduced a new method to retrieve both self and cross correlations in a single call.

- **Bug Fixes** - Improved error handling for cases with no matching features, providing specific
  error messages.

- **Documentation** 	- Updated public API to reflect new method names and signatures. <!-- end of
  auto-generated comment: release notes by coderabbit.ai -->


## v1.30.0 (2024-12-19)

### Features

- Fix loaders some more ([#98](https://github.com/bhklab/readii/pull/98),
  [`6272a03`](https://github.com/bhklab/readii/commit/6272a03fd72b71e00e296ddc002b14b05a70e57f))

Didn't test updating from os to pathlib enough, but should be good now. Added basic test, needs to
  be expanded upon.

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Introduced a new variable for improved file path handling in the feature
  loading process. - Added a comment for clarity on retrieving the full path to the feature file.

- **Bug Fixes** - Updated logic for removing the image type file from the feature files list.

- **Tests** - Added a new test function to validate the functionality of the feature loading
  function. 	- Implemented a fixture for testing with a temporary feature file. <!-- end of
  auto-generated comment: release notes by coderabbit.ai -->


## v1.29.1 (2024-12-18)

### Bug Fixes

- Look for image type in Path stem as Path is not iterable
  ([#97](https://github.com/bhklab/readii/pull/97),
  [`875a6c3`](https://github.com/bhklab/readii/commit/875a6c3cb1c3d10a8225f45f5770380b83562003))

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- **New Features** - Improved file matching logic for identifying features based on image types. -
  Enhanced clarity in handling scenarios for matching files with updated control flow.

- **Bug Fixes** - Retained consistent error handling with appropriate logging for warnings and
  exceptions.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.29.0 (2024-12-18)

### Features

- Add CorrelationWriter ([#96](https://github.com/bhklab/readii/pull/96),
  [`b241c42`](https://github.com/bhklab/readii/commit/b241c42f576ce967ef8463c74f76397b8e99fcf5))

Created CorrelationWriter class for the analyze portion of the pipeline.

I think there will eventually be a FeatureSetWriter that this should probably inherit from, but I
  need the Correlation one now for Aerts.

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Introduced a `CorrelationWriter` class for managing the writing of correlation
  data to files with customizable paths and filenames. - Added support for saving correlation data
  in both CSV and Excel formats.

- **Bug Fixes** - Implemented error handling for invalid correlation data, existing files, and
  filename format validation.

- **Tests** - Added a comprehensive suite of unit tests for the `CorrelationWriter` class, covering
  various scenarios for saving correlation data. <!-- end of auto-generated comment: release notes
  by coderabbit.ai -->

---------

Co-authored-by: Jermiah Joseph <jermiahjoseph98@gmail.com>


## v1.28.0 (2024-12-18)

### Features

- Add io/readers to ruff config ([#94](https://github.com/bhklab/readii/pull/94),
  [`7efc97b`](https://github.com/bhklab/readii/commit/7efc97bfca18c92de5f4a859f96654df53572028))

Updated include list to have the io/readers functions and updated the files so all ruff tests pass.

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Enhanced flexibility in loading feature files by accepting both `Path` objects
  and strings. - Improved error handling and logging for file loading and directory access.

- **Bug Fixes** - Enhanced error handling and logging for file loading and directory access,
  providing clearer context for issues.

- **Documentation** - Updated docstrings for functions to improve clarity and detail, including
  return type annotations. <!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.27.0 (2024-12-17)

### Features

- Add analysis functions ([#92](https://github.com/bhklab/readii/pull/92),
  [`a57182c`](https://github.com/bhklab/readii/commit/a57182cb32f3bcd3600eaed53ad60ac145fe9d6f))

Includes correlation calculations and plotting those correlations as a heatmap and histogram

- **New Features** - Updated version number to 1.26.0 with new dependencies: `numpy`, `seaborn`, and
  `pandas`. - Introduced a new module for analyzing READII outputs with several correlation
  functions. - Added visualization functions for correlation data: heatmap and histogram. 	- New
  validation function for DataFrame dimensions added. 	- Expanded platform support to include
  `osx-64` and `win-64`.

- **Bug Fixes** - Enhanced error handling in correlation calculations and plot saving processes. 	-
  Simplified exception handling in feature loading functions.

- **Documentation** - Improved docstrings for new functions and modules for better usability.

- **Chores** 	- Expanded linting configuration for broader coverage of Python files.


## v1.26.0 (2024-12-16)

### Features

- Expand platform support in pixi and CI/CD workflow
  ([#91](https://github.com/bhklab/readii/pull/91),
  [`546fe5c`](https://github.com/bhklab/readii/commit/546fe5c1e4a4dff72645f2c61730d1acf0d13572))

This PR adds the windows platform and older mac platform to the pixi configuration so developers
  with those machines can be assured that they can contribute to this project without running into
  dependency issues

- also add a testing branch to test with windows across all configured python versions

## Summary by CodeRabbit

- **New Features** 	- Expanded testing environment to include Windows support. 	- Updated project
  version to "1.25.0". 	- Added support for additional platforms: "osx-64" and "win-64".

- **Bug Fixes** - Clarified the checkout process for the publishing jobs in the CI-CD workflow.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.25.0 (2024-12-16)

### Features

- Add optional segmentationLabel input for singleRadiomifFetaureExtraction
  ([#90](https://github.com/bhklab/readii/pull/90),
  [`bebb8f3`](https://github.com/bhklab/readii/commit/bebb8f312c5b1467cedd370c0137f762e5c9c897))

Discovered an edge case when processing ISPY2 SEG files that have multiple regions in them that are
  identified by numeric values in the mask.

Need READII to be able to take a specific value so the correct mask is used when checking the mask,
  cropping the image, and performing feature extraction.

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** - Introduced an optional `segmentationLabel` parameter in the feature extraction
  process for enhanced flexibility. - Improved error handling during segmentation mask validation
  and image cropping.

- **Bug Fixes** - Enhanced robustness by catching and logging exceptions related to feature
  extraction.

- **Tests** - Added new tests to verify behavior with the `segmentationLabel` parameter and to
  validate error handling for invalid inputs. <!-- end of auto-generated comment: release notes by
  coderabbit.ai -->


## v1.24.0 (2024-12-16)

### Features

- Add data functions used for analysis code ([#89](https://github.com/bhklab/readii/pull/89),
  [`2eb6e1e`](https://github.com/bhklab/readii/commit/2eb6e1ebe05597f18be3eac5ae75a8f81d370aea))

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- **New Features** - Introduced functions for manipulating and analyzing patient data, including
  patient ID handling and time conversion. - Added capabilities for selecting and filtering radiomic
  data within DataFrames. - Implemented methods for replacing values and splitting DataFrames based
  on specified criteria.

- **Bug Fixes** - Enhanced error handling across multiple functions to ensure robust performance and
  logging of issues.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->


## v1.23.0 (2024-12-13)

### Features

- Add io/loaders module ([#83](https://github.com/bhklab/readii/pull/83),
  [`81fbd78`](https://github.com/bhklab/readii/commit/81fbd78ea22a089f0c3848a75de3f87aa8a2e5d9))

Includes features, general, and images specific loading functions

- **New Features** - Introduced a new module for loading various data types in the READII pipeline.
  - Added functions for loading imaging feature sets, dataset configurations, and data files into
  DataFrames.


## v1.22.0 (2024-12-13)

### Features

- Add BaseWriter, and example NIFTIWriter with notebooks documenting them
  ([#84](https://github.com/bhklab/readii/pull/84),
  [`7228770`](https://github.com/bhklab/readii/commit/72287708058949f0bd11792878e246c2e1915122))

Mostly inspired and reusing logic from Med-ImageTools `DICOMSorter` design

- **New Features** - Enhanced Jupyter notebooks for saving medical imaging data in NIFTI format and
  CSV metadata. - Added examples for using subclasses of `BaseWriter` for writing text and CSV
  files. - Introduced the `NIFTIWriter` class for managing NIFTI file writing with validation and
  error handling. - Added new `CSVWriter` class for saving data in CSV format.


## v1.21.0 (2024-12-13)

### Features

- Add readii-datasets CLI command and include orcestra-downloader dependency
  ([#80](https://github.com/bhklab/readii/pull/80),
  [`f760b68`](https://github.com/bhklab/readii/commit/f760b6895ff7a6393a2cb6573ecd4bbce9178f40))

closes https://github.com/bhklab/analyze_readii_outputs/issues/6

the CLI in `orcestra-downloader` uses click and allows us to reuse the same user CLI API for just a
  subset of the data and so the `readii-datasets` entry point is just a renamed version of that one
  to prevent rewriting code.


## v1.20.0 (2024-12-12)

### Features

- Initialize documentation ([#85](https://github.com/bhklab/readii/pull/85),
  [`3b2c294`](https://github.com/bhklab/readii/commit/3b2c29404c4266a438dbd8e56b1aef09ffa06b40))

Start of documentation, mostly copied the core dependencies and plugins from med-imagetools

- Set up initial documentation structure using MkDocs, including configuration and integration of
  Markdown files for the README and CHANGELOG.

this "core" would be the base of the main vs 2.0 branch

<!-- This is an auto-generated comment: release notes by coderabbit.ai --> ## Summary by CodeRabbit

- **New Features** 	- Added badges for project health and status in the README. - Expanded
  installation instructions with a new environment setup method. 	- Introduced a section for serving
  documentation locally.

- **Documentation** - Enhanced clarity and structure of the README, including command-line options
  and contributing guidelines. 	- Updated inclusion method for CHANGELOG and README in
  documentation. - Introduced a new configuration file for MkDocs documentation, improving
  navigation and usability.

- **Bug Fixes** - Corrected formatting for bash commands in the README to enhance readability.

- **Chores** 	- Updated project version and dependencies in the configuration files. <!-- end of
  auto-generated comment: release notes by coderabbit.ai -->


## v1.19.0 (2024-12-11)

### Features

- Add abstract and concrete classes for negative controls and regions
  ([#81](https://github.com/bhklab/readii/pull/81),
  [`c10a568`](https://github.com/bhklab/readii/commit/c10a56885213a2c15685db3f8b64dcf4ef454e7a))

# 4D-Lung

![combined](https://github.com/user-attachments/assets/17d071d5-5738-4b08-ac72-d0a7b46e254a)

# Order of operations

1. `negative_control_strategy(image, mask=mask, region=region_strategy)` 2. runs the `__call__` on
  the `negative_control_strategy` 3. which runs the `__call__` of `region(image_array, mask_array)`
  4. the result of which is used to figure out what indices of the original image to apply the
  `transform` method of the `NegativeControlStrategy` concrete classes to 5. only replace the region
  indices `image_array[mask_indices] = transformed_values`

Resource on Strategy Pattern: https://refactoring.guru/design-patterns/strategy/python/example

---------

Co-authored-by: Katy Scott <k.l.scott16@gmail.com>

### Refactoring

- Update Ruff configuration and refactor codebase ([#68](https://github.com/bhklab/readii/pull/68),
  [`e88e704`](https://github.com/bhklab/readii/commit/e88e7049626a976f277b437fa28eafa313f269f1))

Enhance the Ruff configuration to include additional files and ignore specific PEP-8 naming
  conventions. Refactor the codebase by replacing `os.path` with `pathlib`, improving logging
  verbosity, adding type annotations, and organizing imports.

- **Bug Fixes** - Improved error handling for image cropping and feature extraction processes,
  ensuring robustness and clearer logging. - **Chores** - Updated configuration settings to refine
  linting rules and file inclusions, optimizing code quality checks. - Incremented Pixi version
  across CI-CD jobs for improved performance.

- **feature-extraction**: Extract-method refactor to simplify workflow, prepare for class-based
  feature extraction ([#69](https://github.com/bhklab/readii/pull/69),
  [`3bcaa28`](https://github.com/bhklab/readii/commit/3bcaa28dbbbfe229bb41d7391eb059fb26536993))

summary: Refactor code to improve readability, logging, and type annotations while addressing
  various bugs and updating dependencies.

mostly extract-method refactoring to make following code flow a bit easier. - setting up to create a
  class for the module to save from passing around all the parameters

updates to code quality control tasks - for the most part will follow suit with med-imagetools
  configuration for qc - `pixi run qc` will run ruff format and lint on files included in ruff.toml
  - Enhance ruff configuration to include additional files and ignore specific PEP-8 naming
  conventions.

- **New Features** - Introduced new functions for enhanced radiomic feature extraction:
  `generateNegativeControl`, `cropImageAndMask`, and `featureExtraction`.

- **Improvements** - Enhanced error handling and logging for the feature extraction process. -
  Improved documentation and formatting in loaders for better readability.

- **Configuration Updates** - Updated linting configuration to include specific files for checks and
  clarified linting rules with detailed comments. - Updated project version to "1.18.0" and added
  new dependencies for Jupyter-related packages. - Streamlined CI-CD workflow by modifying linting
  commands and removing unnecessary jobs.


## v1.18.0 (2024-11-28)

### Features

- Add slicedim to displayimageslice ([#67](https://github.com/bhklab/readii/pull/67),
  [`c018de5`](https://github.com/bhklab/readii/commit/c018de5cc028fb936b2f20e61afa59f6e966e1d2))

* feat: add slice dimension variable for displayImageSlice

Allows user to indicate whether the slice index is first or last

* build: add libraries to run jupyter notebooks

* docs: fix variable type for sliceDim in displayImageSlice docstring


## v1.17.0 (2024-11-22)

### Features

- Replace get_logger with imgtools inherited logging instance across modules
  ([`01bd13f`](https://github.com/bhklab/readii/commit/01bd13f3321463d627f50254948cc85fd42235a2))


## v1.16.0 (2024-11-13)


## v1.14.1 (2024-11-07)

### Bug Fixes

- Add readii cli entry point to pyproject ([#58](https://github.com/bhklab/readii/pull/58),
  [`1710b72`](https://github.com/bhklab/readii/commit/1710b7294b7e36273a7cc239b97593c676638463))


## v1.14.0 (2024-11-01)

### Features

- Remove dicom-parser, update mit, deprecate padSeg
  ([#51](https://github.com/bhklab/readii/pull/51),
  [`a6658e7`](https://github.com/bhklab/readii/commit/a6658e7fa137b94329ba0dc303d25eab4be4c2f2))

* fix: Update med-imagetools dependency and handle deprecated padSegToMatchCT function in
  feature_extraction.py with error logging

* chore: Update .gitignore to exclude .old, data, and trash directories for working dir

* Update src/readii/feature_extraction.py

Co-authored-by: coderabbitai[bot] <136622811+coderabbitai[bot]@users.noreply.github.com>

* fix: change gitignore data

* better handling of data ignore

---------


## v1.13.2 (2024-10-22)

### Bug Fixes

- Remove hatch config and streamline build settings in pyproject.toml for better package management
  and deployment
  ([`0cf184c`](https://github.com/bhklab/readii/commit/0cf184ce2eca672918b669559c1b47bb53913e55))


## v1.13.1 (2024-10-22)

### Bug Fixes

- Update CI/CD workflow for PyPI publishing; enhance publish step, remove TestPyPI, and configure
  pixi.lock sha256
  ([`743ea52`](https://github.com/bhklab/readii/commit/743ea526a09bf442af79903a84b06c679ec76215))


## v1.13.0 (2024-10-22)

### Bug Fixes

- Correct version location in pyproject.toml configuration
  ([`bdb49ea`](https://github.com/bhklab/readii/commit/bdb49ea83ac6676248cb864e3ab45e95629e9aad))

- Improve modality handling in loadSegmentation by reinforcing RTSTRUCT validation and simplifying
  modality checks
  ([`5d1fef6`](https://github.com/bhklab/readii/commit/5d1fef65288f57e39c40ecb35ac2d81a5d07d31a))

- Update CI/CD workflow to trigger only on pushes to main branch
  ([`2cc686f`](https://github.com/bhklab/readii/commit/2cc686f88d5270a21b97e4e85ea524222cdf77f8))

- Update ruff configuration and linting rules, switch docstring style to numpy, and enhance loader
  type annotations
  ([`0142860`](https://github.com/bhklab/readii/commit/0142860bf572b5e3ff7c3f0132deeabdcd611482))

### Chores

- Add Codecov badge to README for improved visibility of test coverage
  ([`9472ab6`](https://github.com/bhklab/readii/commit/9472ab686f61e990ec85f1023ae1c71ee0a781f2))

- Add Codecov step in CI/CD workflow to track coverage and report using coverage.xml
  ([`fcbe561`](https://github.com/bhklab/readii/commit/fcbe561ce0c6adec16d06eba6f01b1558c7b9eac))

- Add Ruff linter to CI-CD workflow and update project config for linting and formatting tasks
  ([`ecebe9a`](https://github.com/bhklab/readii/commit/ecebe9a6f0ff3333102fb08a7bb4c63f9d2f6175))

- Adjust CI-CD workflow to trigger on any branch for pull requests and comment out previous push
  configuration
  ([`3c77975`](https://github.com/bhklab/readii/commit/3c779750af8b68940236d725264acb4df2e5313c))

- Refine CI-CD workflow for Publish-To-PyPi and update pixi.lock SHA for dependency consistency
  ([`3c904e1`](https://github.com/bhklab/readii/commit/3c904e17ada58031cd10ab37f28ef7ec28aac56f))

### Continuous Integration

- Clean up .github/workflows/ci-cd.yml by removing unnecessary whitespace and ensuring proper
  formatting at end of file
  ([`a6298ab`](https://github.com/bhklab/readii/commit/a6298ab30d7fcb1ead133ef3fbbe31f143a5d36f))

- Update CI-CD workflow to include Ruff as a dependency for the Unit-Tests job before deployment to
  PyPI
  ([`5d6a7f3`](https://github.com/bhklab/readii/commit/5d6a7f3a055120a67eb0ac95dd44c59e7e08e1f4))

### Documentation

- Update README with installation + badges
  ([`7bdf5d3`](https://github.com/bhklab/readii/commit/7bdf5d3a27fad5fa70b92f9fbd63053be7158e29))

### Features

- Enhance segmentation loading by adding validation for unsupported modalities in loadSegmentation
  function
  ([`9ee6931`](https://github.com/bhklab/readii/commit/9ee69315703135ae2951196cb17281a5c2567732))

- Expand pyproject.toml with publish-test command for deploying to test PyPI and add description for
  build task
  ([`f309346`](https://github.com/bhklab/readii/commit/f3093465bdcd079ec403324b9a5f3eb29b8aa967))

- Rename job to Publish-To-Test-PyPi and add Test-TestPypi-Installation steps for verifying package
  deployment
  ([`336185f`](https://github.com/bhklab/readii/commit/336185fb4486de95abe99ad099dd2f714fb42559))

- Update CI-CD workflow to include publishing to TestPyPI with new environment variables for
  authentication
  ([`d645af1`](https://github.com/bhklab/readii/commit/d645af141f1d47fac296c0952c86b71bd0c85a9c))


## v1.12.0 (2024-10-22)

### Chores

- Refactor CI/CD workflow with enhanced job structure and add basic config files for coverage and
  linting
  ([`994fd75`](https://github.com/bhklab/readii/commit/994fd754e489c95ef044714a9b966aec645ead58))

- Update CI/CD workflow to use actions/checkout@v3, fix semantic-release task, and update pixi.lock
  ([`790ae04`](https://github.com/bhklab/readii/commit/790ae04da36e50fd6f7a9087f6f7b7e99c57326f))

### Features

- Add semantic-release workflow for automated versioning and update readii version to 1.11.0 with
  new author email
  ([`92bc4d4`](https://github.com/bhklab/readii/commit/92bc4d4d3d6bc56bf7a92b88d8b876182fdc0197))

- Update to use pixi and pyradiomics-bhklab
  ([`6a67be4`](https://github.com/bhklab/readii/commit/6a67be4ace53c10d4bb98082978ed4bd7413681f))


## v1.11.0 (2024-09-25)

### Bug Fixes

- **feature_extraction**: Actually raise an exception for negative control creation
  ([`e1a9888`](https://github.com/bhklab/readii/commit/e1a98884308e16055db04846932ce133c34779e0))

### Features

- **feature_extraction**: Add logging for error raised when cropping CT and segmentation
  ([`d9d8069`](https://github.com/bhklab/readii/commit/d9d80695a7e28038389aa0caace5b95295aab479))


## v1.10.0 (2024-09-25)

### Bug Fixes

- **feature_extraction**: Actually raise the error for the negative control creation Exception
  ([`f17fbbc`](https://github.com/bhklab/readii/commit/f17fbbc6074ca68e3378ff4d9ac5865a75b04822))

### Features

- **feature_extraction**: Add try catch around cropping image step
  ([`fedf881`](https://github.com/bhklab/readii/commit/fedf88197582e59644da5e9d2974d1e0828bb672))


## v1.9.0 (2024-09-25)

### Documentation

- Add angular commit syntax to README
  ([`c9f76df`](https://github.com/bhklab/readii/commit/c9f76df9b9d10fc7e37cf4738c9f897816fcef2d))

- Clean up angular commit formatting in README
  ([`1f16ad1`](https://github.com/bhklab/readii/commit/1f16ad11c9de5771bc32f3eac399bc30698178ba))

### Features

- **feature_extraction**: Add catch and logging around negative control creation
  ([`a90efac`](https://github.com/bhklab/readii/commit/a90efac732c7fe474cf15885c59ba32c6a8f9b3c))


## v1.8.0 (2024-09-17)

### Features

- Make output directory and parents as needed before saving radiomic output
  ([`bf7600c`](https://github.com/bhklab/readii/commit/bf7600ce681e08eca55fcf4ef6ece028a99ae430))

### Refactoring

- Change output file from feature extraction without negative control to be
  radiomicfeatures_original_datasetname.csv
  ([`7663ce8`](https://github.com/bhklab/readii/commit/7663ce8de4266a29e857d86e6fad0d32cf4dc87a))

### Testing

- **test_feature_extraction**: Updated for new original image feature extraction output
  ([`2e53bc8`](https://github.com/bhklab/readii/commit/2e53bc8916c53795d96db00057fa108f9f9422db))


## v1.7.7 (2024-09-12)

### Bug Fixes

- Remove coloredlogs dependency and logging configuration from the project
  ([`ba8208f`](https://github.com/bhklab/readii/commit/ba8208fc1925533cda8dfccc165c887fc58bc67d))

### Chores

- Update lockfile
  ([`9c5fa18`](https://github.com/bhklab/readii/commit/9c5fa18fd2b4c53d24a66f12d8987b2c4d7a3f28))


## v1.7.6 (2024-08-27)

### Bug Fixes

- Update ci-cd.yml
  ([`13cc197`](https://github.com/bhklab/readii/commit/13cc197546d81be42c3ba4c72c476ba2ad1895a7))


## v1.7.5 (2024-08-20)


## v1.7.4 (2024-08-19)

### Bug Fixes

- Filter out None values and ensure feature results are properly formatted as lists in
  radiomicFeatureExtraction function
  ([`53c68ff`](https://github.com/bhklab/readii/commit/53c68ffc7adc02176e12f78dc1c8a0fd4e2a6283))

- Use Optional for pyradiomicsParamFilePath in feature extraction functions for older python
  versions
  ([`a9aa977`](https://github.com/bhklab/readii/commit/a9aa977dcb78e24bdbbf2cc7fa4c92dbd9c755e7))

### Refactoring

- Address some type annotation errors, and add logging
  ([`79f342e`](https://github.com/bhklab/readii/commit/79f342ef92d9943a08c495946c48d1aa9a6b01ba))

- Simplify negative control region handling by removing unnecessary elif and raising ValueError in
  negative_controls.py
  ([`17ad253`](https://github.com/bhklab/readii/commit/17ad2532f9c5dfdb84b2b91a2b071ff1133d543c))

- Update logging format for better clarity in log messages, put the function name at the end of
  message in brackets to make it easier to read
  ([`bb8aa14`](https://github.com/bhklab/readii/commit/bb8aa14a5c525030663dbace9fe86e8db39c2b9c))


## v1.7.3 (2024-08-19)

### Bug Fixes

- Update CI/CD workflow to specify supported platforms for Docker build, removing unsupported macOS
  entries
  ([`d19bf9b`](https://github.com/bhklab/readii/commit/d19bf9b79840b0921bf6d60be212b2947f7dbb47))


## v1.7.2 (2024-08-19)

### Bug Fixes

- Update base image in Dockerfile to python:3.11-slim to fix docker image errors
  ([`0e2cd3a`](https://github.com/bhklab/readii/commit/0e2cd3a2e7ef29b445ae9d81520739d44672f938))


## v1.7.1 (2024-08-19)

### Bug Fixes

- Using correct pyradiomics in pyproject
  ([`980cdda`](https://github.com/bhklab/readii/commit/980cdda937ee07333d14d80454e3818a4757b556))


## v1.7.0 (2024-08-19)

### Bug Fixes

- **feature_extraction**: Add try except around actual feature extraction call, add logging to end
  of feature extraction and file saving
  ([`ba119ad`](https://github.com/bhklab/readii/commit/ba119adde76c32b9bf04d2199b0c09bbcb07349e))

- **logging**: Enhance metadata file logging output with update flag details and adjust logging
  level to INFO
  ([`3705110`](https://github.com/bhklab/readii/commit/370511086ab57bb7fa92fcd341b01d9aacdcc855))

### Chores

- **deps**: Update dependencies
  ([`0296dbd`](https://github.com/bhklab/readii/commit/0296dbdc687f7e06caed3ef2e2edff16a7cae004))

### Features

- **logging**: Integrate logging for feature extraction and pipeline; replace print statements with
  logger calls
  ([`ed6aed4`](https://github.com/bhklab/readii/commit/ed6aed499fd8d50ca34218e8cfd0b67b4d4b822a))

### Refactoring

- **metadata**: Add createImageMetadataFile function with logging for segmentation; improve error
  handling and directory creation
  ([`7e3d07f`](https://github.com/bhklab/readii/commit/7e3d07f86cd9464e6e146e3bee7968ba5f1d3ba7))


## v1.6.4 (2024-08-14)

### Bug Fixes

- **feature_extraction**: Missed variable name change for non-cropped negative control
  ([`8d0d7bd`](https://github.com/bhklab/readii/commit/8d0d7bd91bb60f669086ef2ef85bf5e210e4ce7d))

### Refactoring

- **feature_extraction**: Move cropping to after negative control creation
  ([`f6e840b`](https://github.com/bhklab/readii/commit/f6e840b5f4b813334a5ec7fb050ac2cb82472564))


## v1.6.3 (2024-08-08)

### Bug Fixes

- **feature_extraction**: Update negative control component splitting for non_roi options to
  properly separate the type and region in singleRadiomicFeatureExtraction
  ([`3bb250e`](https://github.com/bhklab/readii/commit/3bb250e138f7886461bd15613d1bac168c54f3b6))


## v1.6.2 (2024-08-07)

### Bug Fixes

- **feature_extraction**: Negative control component split wouldn't work for
  randomized_sampled_non_roi, so added specific fix for it for now until readii input is updated
  ([`241b202`](https://github.com/bhklab/readii/commit/241b2028f34fd66c0b349c4dbe6e574370a37ecd))


## v1.6.1 (2024-08-06)

### Performance Improvements

- **negative_controls**: Improved efficiency for ROI and Non-ROI negative control generation
  ([`00f3ab2`](https://github.com/bhklab/readii/commit/00f3ab266b16b820a8d92bed52e444ded1feb566))

### Refactoring

- **feature_extraction**: Update for new negative control functions, remove unnecessary imports, add
  print statement when starting feature extraction to differentiate from negative control creation
  ([`5669919`](https://github.com/bhklab/readii/commit/566991945fc4c8ff079149ff6c54759f84fa7920))

### Testing

- **test_negative_controls**: Updated test functions to match new negative control generation
  functions
  ([`fa78177`](https://github.com/bhklab/readii/commit/fa781775c2de8a887464836a526fe770580446ad))


## v1.6.0 (2024-07-31)

### Bug Fixes

- **metadata**: Drop _CT suffix from patient ID column in output of getCTWithSegmentation
  ([`5e31b73`](https://github.com/bhklab/readii/commit/5e31b739e74edab76d4a2d248098e68fed8c2f52))

### Features

- **metadata.py**: Add saving out samples with segmentations to getCTWithSegmentation
  ([`b575f31`](https://github.com/bhklab/readii/commit/b575f3110f1b3be64e635cbe2252c668a6725382))

### Refactoring

- **metdata.py**: In matchCTtoSegmentation change outputDir to outputFilePath
  ([`4219a1a`](https://github.com/bhklab/readii/commit/4219a1ac90673ce7fbfc71c907c6101da8928f97))

- **pipeline.py**: Use new getCTWithSegmentation function, utilizes imgtools edges output
  ([`f1dd879`](https://github.com/bhklab/readii/commit/f1dd8792692dff0dbaa132a47f47bf39e0d53d6a))

### Testing

- **test_metadata**: Added tests for getCTWithSegmentation
  ([`a7d3fc7`](https://github.com/bhklab/readii/commit/a7d3fc7d7181eab5d539eda46fda38a38d51e116))

- **test_metadata**: Fix outputFilePath argument for matchCTtoSegmentation, add output test for
  getCTWithSegmentation
  ([`a9fec18`](https://github.com/bhklab/readii/commit/a9fec1876d649e02c5097f80cf9f37d8d6d9eea0))


## v1.5.0 (2024-07-31)

### Code Style

- **metadata**: Update error message to say READII instead of YAREA
  ([`d6fc791`](https://github.com/bhklab/readii/commit/d6fc7917140bafb645fc07f8a77d582d73dd3410))

### Features

- **metadata.py**: Using imgtools edges crawl output to get matched CT to RTSTRUCT list
  ([`dce17fc`](https://github.com/bhklab/readii/commit/dce17fc4b353a7f3971f5eebaffd79ac5da5a522))


## v1.4.4 (2024-05-30)

### Bug Fixes

- Update docker image reference
  ([`91b3c05`](https://github.com/bhklab/readii/commit/91b3c057507e316df375a5fab34428cc47622922))


## v1.4.3 (2024-05-30)

### Bug Fixes

- Force build
  ([`45cab79`](https://github.com/bhklab/readii/commit/45cab79004e661b955157d7c4284351d532d50b4))

### Chores

- Update dependencies and workflow for continuous deployment
  ([`d400520`](https://github.com/bhklab/readii/commit/d4005204a85adacceea20cf00ceb22f51f684df4))


## v1.4.2 (2024-05-30)

### Bug Fixes

- Tag version in dockerfile
  ([`1b06ed8`](https://github.com/bhklab/readii/commit/1b06ed8a4c196f1e794c34717c700fff75a93f48))


## v1.4.1 (2024-05-30)

### Bug Fixes

- Add auto build docker
  ([`e1a58cd`](https://github.com/bhklab/readii/commit/e1a58cd94c2a2a99b0d71f9a536451b734f4f718))


## v1.4.0 (2024-05-29)

### Features

- **feature_extraction**: Added argument random seed for negative control creation
  ([`053d542`](https://github.com/bhklab/readii/commit/053d54266781863a2c5f285e3aec77a831aa1d28))

- **pipeline**: Added random seed command line argument for negative control creation
  ([`405fa74`](https://github.com/bhklab/readii/commit/405fa74f80c257c8e616d838dcc64b3865ac5bc9))


## v1.3.4 (2024-05-16)

### Bug Fixes

- Poetry lock
  ([`0632d5a`](https://github.com/bhklab/readii/commit/0632d5ae3aa619387f2e3c8ff064c243dd5b3ee4))

- Pyradiomics original
  ([`4ab6aa7`](https://github.com/bhklab/readii/commit/4ab6aa7f7562a34c4ddf91a2697058fc796ee8a8))

- Pyradiomics original
  ([`9513427`](https://github.com/bhklab/readii/commit/9513427f2cf7a9d7a59adb250d8d1a76d5e45773))


## v1.3.3 (2024-05-16)

### Bug Fixes

- Install poetry
  ([`c1a905a`](https://github.com/bhklab/readii/commit/c1a905a7c3304d31e6edddb8332d98701b1ede18))


## v1.3.2 (2024-05-16)

### Bug Fixes

- No docker buils
  ([`e0a8e63`](https://github.com/bhklab/readii/commit/e0a8e63c584d0fcedbd5fcba42523d5d52a22a4d))

- Update lock
  ([`18054bd`](https://github.com/bhklab/readii/commit/18054bdadda30253b29eb06839dccaca356fbf1f))


## v1.3.1 (2024-05-16)

### Bug Fixes

- Update readme with docker link
  ([`4584af7`](https://github.com/bhklab/readii/commit/4584af76e908708e9af1edc4fba0622c8a0ad30c))

fix: update readme with docker link

- Update readme with docker link
  ([`2f9a437`](https://github.com/bhklab/readii/commit/2f9a43707510154f207ff1b1ba31ddb879fb6e2d))


## v1.3.0 (2024-05-16)

### Bug Fixes

- **image_processing**: Correctedroiimage was assigned to unused variabel, changed to segImage
  ([`453402e`](https://github.com/bhklab/readii/commit/453402ed269cf7ec796a7337eae6fedabf07adc4))

- **negative_controls**: Cast result from randNumGen.integers to int for sitk SetPixel function to
  fix type error
  ([`257c498`](https://github.com/bhklab/readii/commit/257c49873ebd73b0829b1b4d940e214c3a9192fe))

- **negative_controls**: Set random generated pixel value to int to work with SetPixel
  ([`8d9b071`](https://github.com/bhklab/readii/commit/8d9b0717428231ff8e8b96c5150953e487ce6038))

- **test_negative_controls**: Makerandomimage test was using incorrect function (shuffleImage)
  ([`143712a`](https://github.com/bhklab/readii/commit/143712a7885d957bbd63552a716b51ecbb4a9704))

### Build System

- **poetry.lock**: Updated package versions
  ([`811b748`](https://github.com/bhklab/readii/commit/811b748184992b090fb96b0ec10ae5768cd6fa1d))

### Code Style

- **feature_extraction**: Fix typo in randomizeImageFromDistributionSampling import
  ([`79dc539`](https://github.com/bhklab/readii/commit/79dc539c6802bc235347e16ba4025c39e3cfef4f))

- **negative_controls**: Fix spelling of distribution in randomizeImageFromDistributionSampling
  ([`4a01f5c`](https://github.com/bhklab/readii/commit/4a01f5cb6eb448429d3cdac236ab06a3c6441282))

### Documentation

- **example.ipynb**: Update notebook to use med-imagetools CT DICOM loader
  ([`e6339b7`](https://github.com/bhklab/readii/commit/e6339b738f8cf05c04f12d5ae88b0e7baabc8685))

- **negative_controls**: Add random seed description to shuffleImage function header
  ([`df9a7d3`](https://github.com/bhklab/readii/commit/df9a7d3fa3cc9992a965e670a0474a19b9291cd2))

### Features

- **negative_controls**: Add random seed to shuffleNonROI
  ([`a402ee5`](https://github.com/bhklab/readii/commit/a402ee57b9300558cd796bffe3ed3d8afa1e1654))

- **negative_controls**: Add random seed to shuffleROI
  ([`826b00d`](https://github.com/bhklab/readii/commit/826b00ddd92ae7fa1e4441426970066de66f8af4))

- **negative_controls**: Added random seed to all random functions and the apply negative control
  function
  ([`280b465`](https://github.com/bhklab/readii/commit/280b46578b6320dd8c9e66ee822dc0ffb7ac9d98))

- **negative_controls**: Added random seed to shuffleImage function, now using numpy RNG and shuffle
  function
  ([`a2556ae`](https://github.com/bhklab/readii/commit/a2556aef0afe87f162bf3f6d12c572af23f9a9dc))

### Testing

- **negative_controls**: Add random seed in shuffleROI test
  ([`d12ac25`](https://github.com/bhklab/readii/commit/d12ac25ba7cfb050017d365ef5d93825469e9a0c))

- **negative_controls**: Add random seed to make random image
  ([`6979ac6`](https://github.com/bhklab/readii/commit/6979ac6b72ac9a33aaa2f9178bf52ff711770478))

- **negative_controls**: Add random seed to shuffle image test
  ([`c07c50e`](https://github.com/bhklab/readii/commit/c07c50e857d2dd3c1fff4a25d6f59f4074a2a784))

- **negative_controls**: Added pixel check for centre of ROI, updated failed assertion message for
  randomSeed pixel checks
  ([`ed3bb17`](https://github.com/bhklab/readii/commit/ed3bb17768842339c5661fcfafebbd1c6efc786f))

- **negative_controls**: Added random seed to rest of functions, changed conversion to pixels to
  include whole image not just region that's been altered
  ([`28db728`](https://github.com/bhklab/readii/commit/28db7280944c3e99dffa56e99fb297e27710d563))

- **negative_controls**: Added random seed to shuffleROI and randomROI tests, updated negative
  control image variable to be clearer
  ([`e09c142`](https://github.com/bhklab/readii/commit/e09c14282427a2c854d06e25b69556b3ae6351ef))

- **negative_controls**: Added tests for no roiLabel input for ROI and non-ROI negative control
  functions
  ([`c083878`](https://github.com/bhklab/readii/commit/c083878e86f8196ccbf2cf15eecb8b6c01f42754))

- **negative_controls**: Fix the shuffle check that the same values exist in the new image in
  shuffleROI
  ([`6de291d`](https://github.com/bhklab/readii/commit/6de291d5c7595a31cfb22869784c6183ab4207ef))

- **negative_controls**: In makeRandomImage, added ROI voxel check, removed random pixel check as
  its covered by the randomSeed checks
  ([`17ca738`](https://github.com/bhklab/readii/commit/17ca7386daf7cb5d3437deb1d5dcca9b665b2d57))

- **negative_controls**: Removed redundant random pixel checks and added some checks for any change
  in the negative controls, updated some assertion failure messages
  ([`4ca434b`](https://github.com/bhklab/readii/commit/4ca434b34eebaf71064d3cc34f758d1bb6321556))

- **negative_controls**: Update assertion comment in shuffle ROI
  ([`0c542f4`](https://github.com/bhklab/readii/commit/0c542f48ff07294e504713e51d6a171dbfb70d1c))

- **negative_controls**: Update whole image pixel checks and remove random pixel checks in
  shuffleNonROI and makeRandomRoi
  ([`b970cbe`](https://github.com/bhklab/readii/commit/b970cbe72a2dc66262a3d3bdac8869a5dd160a59))

- **negative_controls**: Updated nsclcCropped fixture to use getCroppedImages function
  ([`24dafff`](https://github.com/bhklab/readii/commit/24dafff25aeddd0bfded9b7dfbac4bf588ac7870))

- **negative_controls**: Updated shuffle pixel check that values are the same as original
  ([`52dda33`](https://github.com/bhklab/readii/commit/52dda337b321b71b61922bbcb20363cea05c23eb))


## v1.2.1 (2024-03-27)

### Bug Fixes

- No development branch
  ([`e3349db`](https://github.com/bhklab/readii/commit/e3349dbc68dd3f8c4f72afe351148f8af2ef846f))

### Build System

- Add pytest-xdist for development parallel tests
  ([`d52a5a3`](https://github.com/bhklab/readii/commit/d52a5a3189cef9fc7599687f6dc1558378d87506))

- Fix formatting in ci-cd.yml and add back unit tests. Rename jobs for better clarity
  ([`b4d49d5`](https://github.com/bhklab/readii/commit/b4d49d53fcccaa63e0e0d0b720da39f9f1dda3fb))

- Update poetry lock
  ([`6999f20`](https://github.com/bhklab/readii/commit/6999f208f33132e53f6ba42037387ae41070bf07))

- Update pytest command to run tests in parallel
  ([`e8f67b9`](https://github.com/bhklab/readii/commit/e8f67b9108f254431c0542a2812c674578db0794))

### Code Style

- **feature_extraction.py**: Changed some function call spacing
  ([`09331a3`](https://github.com/bhklab/readii/commit/09331a3d7f9b6459ab151b9b3611877c04f4d265))

### Refactoring

- Explicit imports from readii.metadata module for performance
  ([`f91afa4`](https://github.com/bhklab/readii/commit/f91afa43e63daeb06be8d9276c9607453d7fe71c))

- Explicitly import all, nested import * can lead to performance issues
  ([`8054799`](https://github.com/bhklab/readii/commit/80547997d7d2c4c852a0f4f43b61d3c49ebe1f51))

- Fixes, updates, formatting
  ([`998f299`](https://github.com/bhklab/readii/commit/998f299cfb3d29b95afde4f371508da2c6c142b6))

refactor: Fixes, updates, formatting

- Format with black
  ([`07d04d8`](https://github.com/bhklab/readii/commit/07d04d8f1b8bacea29a896557971468446e22bf8))

- Format with black, explicit imports, and update type annotations
  ([`04bada5`](https://github.com/bhklab/readii/commit/04bada5a9d1933f840d647c4ef383329a6e9d2e7))

- Refactor saveDataframeCSV and matchCTtoSegmentation functions, add type hints, and improve error
  handling, format with black
  ([`16a83b9`](https://github.com/bhklab/readii/commit/16a83b9541d717f132f6a32afbeb89db02653c63))

- Refactor type check in test_radiomicFeatureExtraction
  ([`bc0d18d`](https://github.com/bhklab/readii/commit/bc0d18da89907ca82e30eb81fbed1ab1ae475cfe))

- Update type annotations to handle optional parameters, format with black for readability, refactor
  applyNegativeControl function to raise AssertionErrror for optional baseROI, handle edge case and
  raise error if none of the nc_types.
  ([`11f0d92`](https://github.com/bhklab/readii/commit/11f0d92a3f86e1c1db328172d338b92b09654f46))

- Update type annotations.
  ([`c6ee885`](https://github.com/bhklab/readii/commit/c6ee885422df735b3230c5541936d3f71ab17f6c))

- Update version variables in pyproject.toml
  ([`5776e5f`](https://github.com/bhklab/readii/commit/5776e5f0f618c3634d01fb86c685e012bc073a08))


## v1.2.0 (2024-03-15)

### Bug Fixes

- Test builds and update toml to include this branch
  ([`af61beb`](https://github.com/bhklab/readii/commit/af61beba9a677a86695268a55bd2887138fb2c59))

- Test deployment
  ([`aa1dcb4`](https://github.com/bhklab/readii/commit/aa1dcb479720f8eec295071ad0b45aedaaf275d2))

- Wrong group in toml
  ([`b55baab`](https://github.com/bhklab/readii/commit/b55baabb4800e074f0f08684874947052ecb9195))

### Features

- Adding dockerfile and gha to build and deploy
  ([`b7d6b73`](https://github.com/bhklab/readii/commit/b7d6b734ef6b955e5b61ff2d980a08893dc2dddb))


## v1.1.3 (2024-03-06)

### Bug Fixes

- **pipeline**: Need to exit when catching the no segmentation type error
  ([`bd1a93b`](https://github.com/bhklab/readii/commit/bd1a93bf0ac9d1104d3df2a46988b14b3401622b))

### Build System

- Updating package versions
  ([`3f3a593`](https://github.com/bhklab/readii/commit/3f3a59358eaa7b5a81b12b8b45589d17f117df9c))


## v1.1.2 (2024-03-06)

### Documentation

- Update README with randomized sampled negative controls, add description of negative controls
  ([`eaff95d`](https://github.com/bhklab/readii/commit/eaff95df12d71af2dd7d69e59565cf00c3bc3e4e))


## v1.1.1 (2024-02-08)

### Bug Fixes

- Update version number
  ([`3b90606`](https://github.com/bhklab/readii/commit/3b9060652fa39f8480691c5e5edc9e77c61131e9))

### Build System

- Add pyarrow as dependency for pandas
  ([`0050dc1`](https://github.com/bhklab/readii/commit/0050dc156940aaab895a367c57307764d580c7d6))

- Changed pyradiomics dependency to 3.0.1 as 3.1.0 has installation issues
  ([`9c89227`](https://github.com/bhklab/readii/commit/9c89227c7c97dadcacd94b7f450668c046c955a1))

- Update dependencies versions
  ([`8b1af18`](https://github.com/bhklab/readii/commit/8b1af187f9e55dea34685b3a03c0abc80b318035))

- Updated med-imagetools dependency
  ([`ed58b9c`](https://github.com/bhklab/readii/commit/ed58b9cfe726ac0d92d165c2e05bdb32753285a7))

- Updated pyradiomics dependency tp 3.0.1a3
  ([`d780b27`](https://github.com/bhklab/readii/commit/d780b27c7fcb4e05343f8575d63b3b5b4b0ae430))


## v1.1.0 (2024-01-31)

### Bug Fixes

- **image_processing**: Moved crop to top of displayOverlay function to get correct centre slice
  index and array conversion happens after crop
  ([`c1037d9`](https://github.com/bhklab/readii/commit/c1037d9c7a353ab689b5688780a872d18184e2cd))

- **negative_controls**: Fixed function call for randomized_sample_full in applyNegativeControl
  ([`06a2f9c`](https://github.com/bhklab/readii/commit/06a2f9cf14be028ea46e8f29c371fbc7770791e6))

- **pipeline**: Fixed check for existing radiomic features file, had incorrect file name
  ([`1819d3d`](https://github.com/bhklab/readii/commit/1819d3d1e45132c195fed8e06c301005d05e18bf))

### Features

- **image_processing**: Add option to display CT and segmentation cropped to ROI
  ([`120524c`](https://github.com/bhklab/readii/commit/120524c17d89d3a2cee0c168b16243b385217cc2))

- **image_processing**: Made cropping CT and segmentation its own function
  ([`5202cc2`](https://github.com/bhklab/readii/commit/5202cc2113f392a0fce92c555bf58ff3085d3d97))


## v1.0.0 (2024-01-26)


## v0.6.0 (2024-01-19)

### Build System

- Changed package name from YAREA to READII
  ([`3bcb4f9`](https://github.com/bhklab/readii/commit/3bcb4f9d9b1666f4fb3c3f66b4e4913358db25d7))

BREAKING CHANGE: yarea name no longer used

### Documentation

- **README**: Update package headline for READII acronym
  ([`1294d44`](https://github.com/bhklab/readii/commit/1294d44ed87a45567e6a957db77f9738817b37b4))

### Features

- **pipeline**: Change parallel input argument to be false by default
  ([`3f8c46a`](https://github.com/bhklab/readii/commit/3f8c46ade25b16a77cc1ee6175bda039b811561f))

### Breaking Changes

- Yarea name no longer used


## v0.5.0 (2024-01-17)

### Bug Fixes

- **image_processing**: Fixed image vs. imgArray variable mixup in displayImageSlice
  ([`c9ea3d6`](https://github.com/bhklab/readii/commit/c9ea3d6f1ae6637139c41651a3c66d133b6d6c5f))

- **image_processing**: Fixed remaining instances of imgArray variable
  ([`84de500`](https://github.com/bhklab/readii/commit/84de5003d65c8726d925108f087cdba3be9288ad))

### Build System

- Updated dependency versions
  ([`44de606`](https://github.com/bhklab/readii/commit/44de60655fef29716ef5d4edbd6e1e18f8e508d1))

### Documentation

- Require python 3.9 in conda env setup
  ([`480b199`](https://github.com/bhklab/readii/commit/480b1997788be447a53a2699a952df076b7b5262))

- **image_processing**: Wrote docstring for displayCTSegOverlay
  ([`2f69dab`](https://github.com/bhklab/readii/commit/2f69dab8f8d7b7b46f7fbe2175b356a4fb28baf7))

- **pipeline**: Indicate whether flags are true or false by default in help message of parallel and
  update
  ([`311dd5e`](https://github.com/bhklab/readii/commit/311dd5e4f946ba78caaf7c1f0d1ed6dceecd5dcb))

### Features

- **image_processing**: Add function to display CT slice with segmentation overlaid
  ([`73342ef`](https://github.com/bhklab/readii/commit/73342efbd24757ac349124ba332dc26f89544ae9))

- **image_processing**: Add function to find center slice and coordinates of ROI in image
  ([`78d69b2`](https://github.com/bhklab/readii/commit/78d69b227ab1e2006ce46badd2b0a37384f45f40))

### Testing

- **test_image_processing**: Added test for getROICenterCoords
  ([`8745fe7`](https://github.com/bhklab/readii/commit/8745fe752a27204eed7359aed4525c962481d2db))


## v0.4.0 (2024-01-17)

### Documentation

- Add installation and usage details to README
  ([`4281620`](https://github.com/bhklab/readii/commit/4281620f5f791030a020cb4fe91b08318d63426b))

### Features

- Added command line example runs to notebook
  ([`48d8d40`](https://github.com/bhklab/readii/commit/48d8d40e24796491cb6491046b3f12f2424df128))


## v0.3.0 (2023-12-21)

### Bug Fixes

- Change radiomic features file output name
  ([`ea0b963`](https://github.com/bhklab/readii/commit/ea0b963c7c7caa0a39ab6149fa86d8783717bc32))

- Move size mismatch handling back to radiomicFeatureExtraction because image file paths are
  available in that function
  ([`ccbe852`](https://github.com/bhklab/readii/commit/ccbe8524fa69a2334b499512a541c3afa13b430a))

- **feature_extraction**: Add check for None in pyradiomics parameter file spot, use default if
  that's the case
  ([`5340f57`](https://github.com/bhklab/readii/commit/5340f57c8ab18818e6bb45cecda96fcb7aba4f5a))

- **feature_extraction**: Moved error handling into singleRadiomicFeatureExtraction and added catch
  for wrong pyradiomics parameter file
  ([`41a3901`](https://github.com/bhklab/readii/commit/41a39018becde60091ffb113640e180a162d536f))

- **image_processing**: Fixed usage of ctDirPath variable in padSegToMatchCT
  ([`892c8d7`](https://github.com/bhklab/readii/commit/892c8d7629595ce89f2893b004f6f7bc585bab21))

- **test_feature_extraction**: Fixed expected output path for radiomicFeatureExtraction
  ([`53c9db3`](https://github.com/bhklab/readii/commit/53c9db3bc31a35e332f9eeda35b82f42c84f5ab1))

- **yarea**: Renamed this file because it had import issues being named the same as the package
  ([`833c5b4`](https://github.com/bhklab/readii/commit/833c5b460140783d0292b7a1991bca7cbd0e5c64))

### Build System

- Add publish to PyPI back in
  ([`e7f182e`](https://github.com/bhklab/readii/commit/e7f182e6b2da527ca9e0a747557bff1bc9dc0b6b))

- Remove publish to PyPI
  ([`f276b76`](https://github.com/bhklab/readii/commit/f276b767ae452eb7aceb702f607100e1c925c1c8))

- Updated semantic release and added package build steps
  ([`5a51e07`](https://github.com/bhklab/readii/commit/5a51e078a8fbf3c0f14c7d0b429d14b830097142))

- Updated semantic release variables
  ([`5e24044`](https://github.com/bhklab/readii/commit/5e240446bc561cc34640a24d315edaf376cd244f))

### Code Style

- **feature_extraction**: Changed ctFolderPath to ctDirPath for consistency
  ([`b7b452e`](https://github.com/bhklab/readii/commit/b7b452ea2d0c6f930cc727ec026b03de5d539121))

### Documentation

- **pipeline**: Fixed typo in data directory help message
  ([`7a19b5a`](https://github.com/bhklab/readii/commit/7a19b5a3d53ff24a6a800a7bcd75add2aff2d741))

### Features

- Add ability to run pipeline using poetry run
  ([`ced5e67`](https://github.com/bhklab/readii/commit/ced5e6771e3f7b688f2f394f0ec0f8b4ff92bf7a))

- **gitignore**: Ignore vscode directory with configurations
  ([`7e30be2`](https://github.com/bhklab/readii/commit/7e30be22e0a56c6f5f438e7ff51ebc9ba2b900f3))

- **metadata**: Added check for csv type on imgFileListPath argument
  ([`ac09625`](https://github.com/bhklab/readii/commit/ac09625fd36622e5a0388ce8e4e74209ed4c9c4c))

- **metadata**: Made function to find the segmentation type from the list of image files
  ([`8dd4ddf`](https://github.com/bhklab/readii/commit/8dd4ddf858c47377d6bac0e9853282772d15dd43))

- **pipeline**: Main pipeline function to run radiomic feature extraction
  ([`929573d`](https://github.com/bhklab/readii/commit/929573d50a22746fae29beceacd8d0169cd3dde3))

### Testing

- **test_metadata**: Testing for getSegmentationType function
  ([`57768cf`](https://github.com/bhklab/readii/commit/57768cfe22fa0a7a3a59b65e25fe768848025ce0))


## v0.2.0 (2023-12-19)

### Bug Fixes

- Fixed default Pyradiomics parameter file path
  ([`84f16db`](https://github.com/bhklab/readii/commit/84f16db1d0032fa81dbf7b30422a74a0ec386984))

- Fixed inconsistencies and mistakes in variable names
  ([`7dd0d30`](https://github.com/bhklab/readii/commit/7dd0d3050916b4c2b1945ca772342f9599cc1b03))

- Fixed pyradiomics parameter file path and moved print statement of which ROI is processed back to
  radiomicFeatureExtraction
  ([`427eff7`](https://github.com/bhklab/readii/commit/427eff77663c66f919cfe239ae10b9080e4b0ef1))

- Forgot to import pytest
  ([`6e978ca`](https://github.com/bhklab/readii/commit/6e978ca088971fe2ef80be629dcc6d7556c7cbd7))

- Incorrect indent in saveDataframeCSV
  ([`dd6d2f5`](https://github.com/bhklab/readii/commit/dd6d2f51bb55ae5bf5940b511862a7800c4a4fe1))

- Missing pytest import and passing flattened SEG to alignImages
  ([`bab47e4`](https://github.com/bhklab/readii/commit/bab47e48a1f71d2ad8cde43ab9640c83b1337e00))

- Need to see test outputs for actions
  ([`6e95d0e`](https://github.com/bhklab/readii/commit/6e95d0e287a105c9f71d2f245fcdf10719913daf))

- Rtstruct loader had incorrect variable for baseImageDirPath
  ([`6cfb08c`](https://github.com/bhklab/readii/commit/6cfb08cb52314931e98a71e3e9de5e0906debeb3))

- Updated image file paths
  ([`588ba46`](https://github.com/bhklab/readii/commit/588ba465ce459c64a62857ca97830def18a8f4cf))

- Was missing pytest import
  ([`b38e7a4`](https://github.com/bhklab/readii/commit/b38e7a492a2bfd435ce21c4755268006cb226c44))

### Build System

- Add med-imagetools as a dependency
  ([`84aef0f`](https://github.com/bhklab/readii/commit/84aef0fe589a1177e8145e30f7b6df15b79de140))

- Add PSR as dev dependency
  ([`17cb2da`](https://github.com/bhklab/readii/commit/17cb2da3352995c9e716733c79fb1bb8f09de23f))

- Add pyradiomics dependency
  ([`cb11289`](https://github.com/bhklab/readii/commit/cb11289446aad3d1f0b7d874af0b17189fce0959))

### Features

- Add function to match CTs and segmentations in medimagetools output and function to save out
  dataframe as csv
  ([`2f169e9`](https://github.com/bhklab/readii/commit/2f169e9eadae4f6a8fb73d34c48f03c7e652f991))

- Add negative control generator functions
  ([`da6d9c0`](https://github.com/bhklab/readii/commit/da6d9c01275d399cb27191dc5eff21165107336b))

- Add seg label finder function
  ([`d575dee`](https://github.com/bhklab/readii/commit/d575dee223c8908eaedaa41312d361f113c9f768))

- Added check for input not being a dataframe for saveDataframeCSV
  ([`69a0d84`](https://github.com/bhklab/readii/commit/69a0d84c1ab83487b059cf72d3d523d22cc37dc9))

- Added example pyradiomics config
  ([`2dee2eb`](https://github.com/bhklab/readii/commit/2dee2eb6ad5c355dec80ec8a72de7ff988077dbb))

- Changed input variable to outputDirPath to have consistent output file name
  ([`a0b3336`](https://github.com/bhklab/readii/commit/a0b33368c983b5f62993d46e0a06f295ac9951a4))

- Changed outputFilePath to outputDirPath so output files can be standardized
  ([`d3ad8e8`](https://github.com/bhklab/readii/commit/d3ad8e8312dacb2315aace95722da777c3013e14))

- Check that output file is a csv before starting any feature extraction
  ([`d2390f5`](https://github.com/bhklab/readii/commit/d2390f50c0bd0f14b13e1eda1729f20c0ca4f9b4))

- Function for extraction of radiomic features from a single CT and segmentation pair
  ([`ecb5d5b`](https://github.com/bhklab/readii/commit/ecb5d5bd4c5ba143622f4db9bfff350a5dc70e05))

- Function to run radiomic feature extraction, including negative control and parallel options
  ([`aeb6efd`](https://github.com/bhklab/readii/commit/aeb6efdcdea607738efe33437e443d5bc92d59c7))

- Ignore unit test output files
  ([`a3fd21e`](https://github.com/bhklab/readii/commit/a3fd21eaacc43d7d1b8571c71f91b4bde0e8a530))

### Testing

- Add getROIVoxelLabel test
  ([`2571cea`](https://github.com/bhklab/readii/commit/2571cea7c363f86716eb986588f746430502fb24))

- Add load segmentation module tests
  ([`6137f61`](https://github.com/bhklab/readii/commit/6137f6199628de184fc0b914871f0f1ee1059a07))

- Added image path fixtures and error check test
  ([`2b69fa1`](https://github.com/bhklab/readii/commit/2b69fa132e9f38868cfe895b6d29606ca6735d4f))

- Added image_processing unit tests
  ([`587eb2a`](https://github.com/bhklab/readii/commit/587eb2affeff25a4dfa59a2532029ec7989c9ecb))

- Added incorrect object passed to saveDataframeCSV and fixed outputFilePath error test function
  call
  ([`281637b`](https://github.com/bhklab/readii/commit/281637b073dec5b1317a9d1bba627f036e552b64))

- Added test for full radiomicFeatureExtraction function
  ([`ade890c`](https://github.com/bhklab/readii/commit/ade890cb2a1c8fd90f4fac433ade2c31e15f42a2))

- Added tests for matchCTtoSegmentation function
  ([`c66d24c`](https://github.com/bhklab/readii/commit/c66d24c77910aaa8af515cb0ece7dcf283de7628))

- Check output from radiomicFeatureExtraction
  ([`c525247`](https://github.com/bhklab/readii/commit/c525247f88029b70f17b1249fd2fdedfa6eb3ddf))

- Functions for singleRadiomicFeatureExtraction
  ([`37ec5d6`](https://github.com/bhklab/readii/commit/37ec5d6e587642895a5f59faf773b305ad02480e))

- Started writing tests for radiomic feature extraction functions
  ([`cd31b86`](https://github.com/bhklab/readii/commit/cd31b86fda9bbca1c86111fcd9bd6ea0ff824daf))

- Test csv error in saveDataframeCSV
  ([`3a9929a`](https://github.com/bhklab/readii/commit/3a9929a53b67291b0da46b4f53a82515d4df364b))

- Test output saving for matchCTtoSegmentation
  ([`995726d`](https://github.com/bhklab/readii/commit/995726dbff3a8e6e2a74de3e0e12e9f35e11a7a6))

- Updated test for radiomicFeatureExtraction to use default pyradiomics parameter file
  ([`617abbc`](https://github.com/bhklab/readii/commit/617abbcbf732433c08475652242830b6592fa321))


## v0.1.0 (2023-11-23)

### Bug Fixes

- Correct conversion of sitk Image to array
  ([`34ddb65`](https://github.com/bhklab/readii/commit/34ddb6525983e69996671940e9f13f5107c69369))

- Updated segImagePath variable
  ([`166831c`](https://github.com/bhklab/readii/commit/166831ccfb0c37b4e057dde254cc387e6a016fc6))

### Build System

- Add loading and image processing dependencies
  ([`96fd62f`](https://github.com/bhklab/readii/commit/96fd62f9794c3a97d84d7b5e1c112c1f8a32cbd0))

- Add pytest and pytest-cov as dev dependencies
  ([`152b825`](https://github.com/bhklab/readii/commit/152b825929a8c0982dd6d5210a14fb891d5b6396))

- Added dev dependencies for docs
  ([`0e87a13`](https://github.com/bhklab/readii/commit/0e87a13807786bfb59aad4e5be9e9812033274fb))

- Remove upper bound on dependency versions
  ([`62ba9f8`](https://github.com/bhklab/readii/commit/62ba9f8f0ec84e8270083f7e82ffcecd30b8dd99))

### Documentation

- Updated docstrings for all functions
  ([`dbe6b84`](https://github.com/bhklab/readii/commit/dbe6b84ac9ecec6a5e5c2282d10ead56085de197))

- Updated example
  ([`794530e`](https://github.com/bhklab/readii/commit/794530e2309a448aea4e3775957dcd2e1f95f0ce))

### Features

- Add image loader functions
  ([`73f67f5`](https://github.com/bhklab/readii/commit/73f67f55dbb59c5967f0d70cd7d7d146118e634e))

- Added image processing functions
  ([`b0ac044`](https://github.com/bhklab/readii/commit/b0ac04443cdf39addc601678cea5f49f44f1f89f))

### Testing

- Add unit test for loadDicomSITK
  ([`bef39f7`](https://github.com/bhklab/readii/commit/bef39f731363d1693f859ffbcdd6686540c1e98d))
