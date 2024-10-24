# CHANGELOG


## v1.13.2 (2024-10-22)

### Bug Fixes

* fix: Remove hatch config and streamline build settings in pyproject.toml for better package management and deployment ([`0cf184c`](https://github.com/bhklab/readii/commit/0cf184ce2eca672918b669559c1b47bb53913e55))


## v1.13.1 (2024-10-22)

### Bug Fixes

* fix: Update CI/CD workflow for PyPI publishing; enhance publish step, remove TestPyPI, and configure pixi.lock sha256 ([`743ea52`](https://github.com/bhklab/readii/commit/743ea526a09bf442af79903a84b06c679ec76215))


## v1.13.0 (2024-10-22)

### Bug Fixes

* fix: update CI/CD workflow to trigger only on pushes to main branch ([`2cc686f`](https://github.com/bhklab/readii/commit/2cc686f88d5270a21b97e4e85ea524222cdf77f8))

* fix: correct version location in pyproject.toml configuration ([`bdb49ea`](https://github.com/bhklab/readii/commit/bdb49ea83ac6676248cb864e3ab45e95629e9aad))

* fix: improve modality handling in loadSegmentation by reinforcing RTSTRUCT validation and simplifying modality checks ([`5d1fef6`](https://github.com/bhklab/readii/commit/5d1fef65288f57e39c40ecb35ac2d81a5d07d31a))

* fix: update ruff configuration and linting rules, switch docstring style to numpy, and enhance loader type annotations ([`0142860`](https://github.com/bhklab/readii/commit/0142860bf572b5e3ff7c3f0132deeabdcd611482))

### Chores

* chore: refine CI-CD workflow for Publish-To-PyPi and update pixi.lock SHA for dependency consistency ([`3c904e1`](https://github.com/bhklab/readii/commit/3c904e17ada58031cd10ab37f28ef7ec28aac56f))

* chore: add Ruff linter to CI-CD workflow and update project config for linting and formatting tasks ([`ecebe9a`](https://github.com/bhklab/readii/commit/ecebe9a6f0ff3333102fb08a7bb4c63f9d2f6175))

* chore: adjust CI-CD workflow to trigger on any branch for pull requests and comment out previous push configuration ([`3c77975`](https://github.com/bhklab/readii/commit/3c779750af8b68940236d725264acb4df2e5313c))

* chore: add Codecov badge to README for improved visibility of test coverage ([`9472ab6`](https://github.com/bhklab/readii/commit/9472ab686f61e990ec85f1023ae1c71ee0a781f2))

* chore: add Codecov step in CI/CD workflow to track coverage and report using coverage.xml ([`fcbe561`](https://github.com/bhklab/readii/commit/fcbe561ce0c6adec16d06eba6f01b1558c7b9eac))

### Continuous Integration

* ci: clean up .github/workflows/ci-cd.yml by removing unnecessary whitespace and ensuring proper formatting at end of file ([`a6298ab`](https://github.com/bhklab/readii/commit/a6298ab30d7fcb1ead133ef3fbbe31f143a5d36f))

* ci: update CI-CD workflow to include Ruff as a dependency for the Unit-Tests job before deployment to PyPI ([`5d6a7f3`](https://github.com/bhklab/readii/commit/5d6a7f3a055120a67eb0ac95dd44c59e7e08e1f4))

### Documentation

* docs: update README with installation + badges ([`7bdf5d3`](https://github.com/bhklab/readii/commit/7bdf5d3a27fad5fa70b92f9fbd63053be7158e29))

### Features

* feat: enhance segmentation loading by adding validation for unsupported modalities in loadSegmentation function ([`9ee6931`](https://github.com/bhklab/readii/commit/9ee69315703135ae2951196cb17281a5c2567732))

* feat: rename job to Publish-To-Test-PyPi and add Test-TestPypi-Installation steps for verifying package deployment ([`336185f`](https://github.com/bhklab/readii/commit/336185fb4486de95abe99ad099dd2f714fb42559))

* feat: update CI-CD workflow to include publishing to TestPyPI with new environment variables for authentication ([`d645af1`](https://github.com/bhklab/readii/commit/d645af141f1d47fac296c0952c86b71bd0c85a9c))

* feat: expand pyproject.toml with publish-test command for deploying to test PyPI and add description for build task ([`f309346`](https://github.com/bhklab/readii/commit/f3093465bdcd079ec403324b9a5f3eb29b8aa967))

### Unknown

* Merge pull request #42 from bhklab/jjjermiah/refactor/main

feat: Enhance CI/CD Workflow with TestPyPI Publishing, Linting Improvements, and minor docs update ([`376b414`](https://github.com/bhklab/readii/commit/376b4140feb49c1470f7f3b639824e08f7c8e046))

* doc: enhance docstrings in loaders.py, providing clearer descriptions and improving module documentation for DICOM and RTSTRUCT functions ([`249238c`](https://github.com/bhklab/readii/commit/249238ca60ef8e7ebaff65d85c5eaf755e7d5616))


## v1.12.0 (2024-10-22)

### Chores

* chore: update CI/CD workflow to use actions/checkout@v3, fix semantic-release task, and update pixi.lock ([`790ae04`](https://github.com/bhklab/readii/commit/790ae04da36e50fd6f7a9087f6f7b7e99c57326f))

* chore: refactor CI/CD workflow with enhanced job structure and add basic config files for coverage and linting ([`994fd75`](https://github.com/bhklab/readii/commit/994fd754e489c95ef044714a9b966aec645ead58))

### Features

* feat: add semantic-release workflow for automated versioning and update readii version to 1.11.0 with new author email ([`92bc4d4`](https://github.com/bhklab/readii/commit/92bc4d4d3d6bc56bf7a92b88d8b876182fdc0197))

* feat: update to use pixi and pyradiomics-bhklab ([`6a67be4`](https://github.com/bhklab/readii/commit/6a67be4ace53c10d4bb98082978ed4bd7413681f))

### Unknown

* Merge pull request #40 from bhklab/jjjermiah/add-pixi

feat: Use Pixi, pyradiomics fork ([`fd582a5`](https://github.com/bhklab/readii/commit/fd582a5db16b3474df798f948c7f533bbb23dc86))


## v1.11.0 (2024-09-25)

### Bug Fixes

* fix(feature_extraction): actually raise an exception for negative control creation ([`e1a9888`](https://github.com/bhklab/readii/commit/e1a98884308e16055db04846932ce133c34779e0))

### Features

* feat(feature_extraction): add logging for error raised when cropping CT and segmentation ([`d9d8069`](https://github.com/bhklab/readii/commit/d9d80695a7e28038389aa0caace5b95295aab479))

### Unknown

* Merge pull request #39 from bhklab/negative_control_error_handling

Negative control error handling ([`2bac7db`](https://github.com/bhklab/readii/commit/2bac7db3d88c24af8b24233b59ec4a62ee5dacaa))

* Merge branch 'main' of github.com:bhklab/yarea into main ([`556178e`](https://github.com/bhklab/readii/commit/556178ed18e9507f25dfd896cb68567298918323))


## v1.10.0 (2024-09-25)

### Bug Fixes

* fix(feature_extraction): actually raise the error for the negative control creation Exception ([`f17fbbc`](https://github.com/bhklab/readii/commit/f17fbbc6074ca68e3378ff4d9ac5865a75b04822))

### Features

* feat(feature_extraction): add try catch around cropping image step ([`fedf881`](https://github.com/bhklab/readii/commit/fedf88197582e59644da5e9d2974d1e0828bb672))

### Unknown

* Revert "1.9.0" ([`c4d265c`](https://github.com/bhklab/readii/commit/c4d265c02e9b49fd806d3f7c4e05ef665db9453e))

* Revert "1.9.0"

This reverts commit 50794f4f143cd980421ee3099ea11fa7900976af. ([`cd37991`](https://github.com/bhklab/readii/commit/cd3799167091f6960dd4e14b3cc77a081e9af905))


## v1.9.0 (2024-09-25)

### Documentation

* docs: clean up angular commit formatting in README ([`1f16ad1`](https://github.com/bhklab/readii/commit/1f16ad11c9de5771bc32f3eac399bc30698178ba))

* docs: add angular commit syntax to README ([`c9f76df`](https://github.com/bhklab/readii/commit/c9f76df9b9d10fc7e37cf4738c9f897816fcef2d))

### Features

* feat(feature_extraction): add catch and logging around negative control creation ([`a90efac`](https://github.com/bhklab/readii/commit/a90efac732c7fe474cf15885c59ba32c6a8f9b3c))

### Unknown

* Merge pull request #38 from bhklab/add_logging

Negative control error catching and angular commit syntax ([`8646cf0`](https://github.com/bhklab/readii/commit/8646cf03f77a50ecd4f0ae66997379093f6719f9))

* Merge pull request #37 from bhklab/keep_running_flag

Created keep_running flag ([`0c95c80`](https://github.com/bhklab/readii/commit/0c95c8025567c47e2b98bdfb98d069e645edb765))

* Added logging ([`f666b4d`](https://github.com/bhklab/readii/commit/f666b4d6be906122636dde727016c7583203f3d9))

* Created keep_running flag, which keeps pipeline running even if a single patient fails. ([`c1fe170`](https://github.com/bhklab/readii/commit/c1fe17097809977fc16b495eb1ec3016a262c8a1))


## v1.8.0 (2024-09-17)

### Features

* feat: make output directory and parents as needed before saving radiomic output ([`bf7600c`](https://github.com/bhklab/readii/commit/bf7600ce681e08eca55fcf4ef6ece028a99ae430))

### Refactoring

* refactor: change output file from feature extraction without negative control to be radiomicfeatures_original_datasetname.csv ([`7663ce8`](https://github.com/bhklab/readii/commit/7663ce8de4266a29e857d86e6fad0d32cf4dc87a))

### Testing

* test(test_feature_extraction): updated for new original image feature extraction output ([`2e53bc8`](https://github.com/bhklab/readii/commit/2e53bc8916c53795d96db00057fa108f9f9422db))

### Unknown

* Merge pull request #36 from bhklab/change-original-image-output-name-convention

Change original image output name convention ([`d6af655`](https://github.com/bhklab/readii/commit/d6af65553f97b8f7b7939a1660d75c6404ce313f))


## v1.7.7 (2024-09-12)

### Bug Fixes

* fix: Remove coloredlogs dependency and logging configuration from the project ([`ba8208f`](https://github.com/bhklab/readii/commit/ba8208fc1925533cda8dfccc165c887fc58bc67d))

### Chores

* chore: update lockfile ([`9c5fa18`](https://github.com/bhklab/readii/commit/9c5fa18fd2b4c53d24a66f12d8987b2c4d7a3f28))

### Unknown

* Merge pull request #35 from bhklab/remove_colored_logs

fix: Remove coloredlogs dependency and logging configuration from the project ([`7616d88`](https://github.com/bhklab/readii/commit/7616d882119e8d608846ab80e875d58f16973aba))


## v1.7.6 (2024-08-27)

### Bug Fixes

* fix: Update ci-cd.yml ([`13cc197`](https://github.com/bhklab/readii/commit/13cc197546d81be42c3ba4c72c476ba2ad1895a7))


## v1.7.5 (2024-08-20)

### Unknown

* Merge pull request #34 from bhklab/add_logging

fix(feature_extraction): add try except around actual feature extract… ([`3e6f211`](https://github.com/bhklab/readii/commit/3e6f211055fd8bcf9a80f8b8dffeb05d60ce88bf))

* Merge branch 'main' into add_logging ([`e36ac1b`](https://github.com/bhklab/readii/commit/e36ac1b610f45822652ccd5d517dfa44d800bc44))


## v1.7.4 (2024-08-19)

### Bug Fixes

* fix: use Optional for  pyradiomicsParamFilePath in feature extraction functions for older python versions ([`a9aa977`](https://github.com/bhklab/readii/commit/a9aa977dcb78e24bdbbf2cc7fa4c92dbd9c755e7))

* fix: filter out None values and ensure feature results are properly formatted as lists in radiomicFeatureExtraction function ([`53c68ff`](https://github.com/bhklab/readii/commit/53c68ffc7adc02176e12f78dc1c8a0fd4e2a6283))

### Refactoring

* refactor: simplify negative control region handling by removing unnecessary elif and raising ValueError in negative_controls.py ([`17ad253`](https://github.com/bhklab/readii/commit/17ad2532f9c5dfdb84b2b91a2b071ff1133d543c))

* refactor: update logging format for better clarity in log messages, put the function name at the end of message in brackets to make it easier to read ([`bb8aa14`](https://github.com/bhklab/readii/commit/bb8aa14a5c525030663dbace9fe86e8db39c2b9c))

* refactor: address some type annotation errors, and add logging ([`79f342e`](https://github.com/bhklab/readii/commit/79f342ef92d9943a08c495946c48d1aa9a6b01ba))

### Unknown

* Merge pull request #33 from bhklab/feature_extraction_typeannt

fix: type annotations & refactor typing issues ([`b1ce1ed`](https://github.com/bhklab/readii/commit/b1ce1ed6c618d506305fc5bdff778fec80a3646e))


## v1.7.3 (2024-08-19)

### Bug Fixes

* fix: update CI/CD workflow to specify supported platforms for Docker build, removing unsupported macOS entries ([`d19bf9b`](https://github.com/bhklab/readii/commit/d19bf9b79840b0921bf6d60be212b2947f7dbb47))


## v1.7.2 (2024-08-19)

### Bug Fixes

* fix: update base image in Dockerfile to python:3.11-slim to fix docker image errors ([`0e2cd3a`](https://github.com/bhklab/readii/commit/0e2cd3a2e7ef29b445ae9d81520739d44672f938))


## v1.7.1 (2024-08-19)

### Bug Fixes

* fix: using correct pyradiomics in pyproject ([`980cdda`](https://github.com/bhklab/readii/commit/980cdda937ee07333d14d80454e3818a4757b556))


## v1.7.0 (2024-08-19)

### Bug Fixes

* fix(feature_extraction): add try except around actual feature extraction call, add logging to end of feature extraction and file saving ([`ba119ad`](https://github.com/bhklab/readii/commit/ba119adde76c32b9bf04d2199b0c09bbcb07349e))

* fix(logging): enhance metadata file logging output with update flag details and adjust logging level to INFO ([`3705110`](https://github.com/bhklab/readii/commit/370511086ab57bb7fa92fcd341b01d9aacdcc855))

### Chores

* chore(deps): update dependencies ([`0296dbd`](https://github.com/bhklab/readii/commit/0296dbdc687f7e06caed3ef2e2edff16a7cae004))

### Features

* feat(logging): integrate logging for feature extraction and pipeline; replace print statements with logger calls ([`ed6aed4`](https://github.com/bhklab/readii/commit/ed6aed499fd8d50ca34218e8cfd0b67b4d4b822a))

### Refactoring

* refactor(metadata): add createImageMetadataFile function with logging for segmentation; improve error handling and directory creation ([`7e3d07f`](https://github.com/bhklab/readii/commit/7e3d07f86cd9464e6e146e3bee7968ba5f1d3ba7))

### Unknown

* Merge pull request #31 from bhklab/add_logging

feat: Add_logging ([`1255e97`](https://github.com/bhklab/readii/commit/1255e97a97b06a231ab70e69f8f6d09dfc940b03))


## v1.6.4 (2024-08-14)

### Bug Fixes

* fix(feature_extraction): missed variable name change for non-cropped negative control ([`8d0d7bd`](https://github.com/bhklab/readii/commit/8d0d7bd91bb60f669086ef2ef85bf5e210e4ce7d))

### Refactoring

* refactor(feature_extraction): move cropping to after negative control creation ([`f6e840b`](https://github.com/bhklab/readii/commit/f6e840b5f4b813334a5ec7fb050ac2cb82472564))

### Unknown

* Merge pull request #30 from bhklab/development_katy

fix(feature_extraction): missed variable name change for non-cropped … ([`ffe6e47`](https://github.com/bhklab/readii/commit/ffe6e4751ed18fb9175db45ea2647d941895a6c4))

* Merge pull request #29 from bhklab/development_katy

refactor(feature_extraction): move cropping to after negative control… ([`f8db5b0`](https://github.com/bhklab/readii/commit/f8db5b06c47c68d6c1759541b59856b0f5354a3d))


## v1.6.3 (2024-08-08)

### Bug Fixes

* fix(feature_extraction): update negative control component splitting for non_roi options to properly separate the type and region in singleRadiomicFeatureExtraction ([`3bb250e`](https://github.com/bhklab/readii/commit/3bb250e138f7886461bd15613d1bac168c54f3b6))

### Unknown

* Merge pull request #28 from bhklab/development_katy

fix(feature_extraction): update negative control component splitting … ([`fc6d13d`](https://github.com/bhklab/readii/commit/fc6d13d4b14b6f299bb46f24585a58f86ce5d3ef))


## v1.6.2 (2024-08-07)

### Bug Fixes

* fix(feature_extraction): negative control component split wouldn't work for randomized_sampled_non_roi, so added specific fix for it for now until readii input is updated ([`241b202`](https://github.com/bhklab/readii/commit/241b2028f34fd66c0b349c4dbe6e574370a37ecd))

### Unknown

* Merge pull request #27 from bhklab/development_katy

fix(feature_extraction): negative control component split wouldn't wo… ([`55dac25`](https://github.com/bhklab/readii/commit/55dac2572bf2ff1e8373169d88c0105359693baf))


## v1.6.1 (2024-08-06)

### Performance Improvements

* perf(negative_controls): improved efficiency for ROI and Non-ROI negative control generation ([`00f3ab2`](https://github.com/bhklab/readii/commit/00f3ab266b16b820a8d92bed52e444ded1feb566))

### Refactoring

* refactor(feature_extraction): update for new negative control functions, remove unnecessary imports, add print statement when starting feature extraction to differentiate from negative control creation ([`5669919`](https://github.com/bhklab/readii/commit/566991945fc4c8ff079149ff6c54759f84fa7920))

### Testing

* test(test_negative_controls): updated test functions to match new negative control generation functions ([`fa78177`](https://github.com/bhklab/readii/commit/fa781775c2de8a887464836a526fe770580446ad))

### Unknown

* Merge pull request #26 from bhklab/development_katy

Improved efficiency negative control functions ([`8d9bcb6`](https://github.com/bhklab/readii/commit/8d9bcb65813f9a158395f684c0236af05f8c2265))

* notebook(optimize_negative_controls): code to develop improved negative control functions ([`d5c396b`](https://github.com/bhklab/readii/commit/d5c396be1217de08df5991fa3c5e9d860059fb34))

* Coded up improved speed functions for ROI and Non-ROI negative control generation using matrix math ([`bc825cd`](https://github.com/bhklab/readii/commit/bc825cdee4b6970abd453ab2b761a2f52554e4e9))


## v1.6.0 (2024-07-31)

### Bug Fixes

* fix(metadata): drop _CT suffix from patient ID column in output of getCTWithSegmentation ([`5e31b73`](https://github.com/bhklab/readii/commit/5e31b739e74edab76d4a2d248098e68fed8c2f52))

### Features

* feat(metadata.py): add saving out samples with segmentations to getCTWithSegmentation ([`b575f31`](https://github.com/bhklab/readii/commit/b575f3110f1b3be64e635cbe2252c668a6725382))

### Refactoring

* refactor(pipeline.py): use new getCTWithSegmentation function, utilizes imgtools edges output ([`f1dd879`](https://github.com/bhklab/readii/commit/f1dd8792692dff0dbaa132a47f47bf39e0d53d6a))

* refactor(metdata.py): in matchCTtoSegmentation change outputDir to outputFilePath ([`4219a1a`](https://github.com/bhklab/readii/commit/4219a1ac90673ce7fbfc71c907c6101da8928f97))

### Testing

* test(test_metadata): fix outputFilePath argument for matchCTtoSegmentation, add output test for getCTWithSegmentation ([`a9fec18`](https://github.com/bhklab/readii/commit/a9fec1876d649e02c5097f80cf9f37d8d6d9eea0))

* test(test_metadata): added tests for getCTWithSegmentation ([`a7d3fc7`](https://github.com/bhklab/readii/commit/a7d3fc7d7181eab5d539eda46fda38a38d51e116))

### Unknown

* Merge pull request #25 from bhklab/development_katy

New get CT with RTSTRUCTs function ([`5c31b26`](https://github.com/bhklab/readii/commit/5c31b26dbb7400b90620dbf2f79ad4f52eaa103b))

* getCTWithSegmentation works for RTSTRUCT ([`6c69b8a`](https://github.com/bhklab/readii/commit/6c69b8a6c5a9123af6b5695ee7baba4523ead50c))

* getCTWithSegmentation works for RTSTRUCT ([`bd8d0a0`](https://github.com/bhklab/readii/commit/bd8d0a074db517b84434bb523df956782adf45df))


## v1.5.0 (2024-07-31)

### Code Style

* style(metadata): Update error message to say READII instead of YAREA ([`d6fc791`](https://github.com/bhklab/readii/commit/d6fc7917140bafb645fc07f8a77d582d73dd3410))

### Features

* feat(metadata.py): using imgtools edges crawl output to get matched CT to RTSTRUCT list ([`dce17fc`](https://github.com/bhklab/readii/commit/dce17fc4b353a7f3971f5eebaffd79ac5da5a522))

### Unknown

* Merge pull request #24 from bhklab/development_katy

New CT to RTSTRUCT matching method and start of testing new negative control generation method ([`c3533a0`](https://github.com/bhklab/readii/commit/c3533a0c21b02d32187fa375505fded3a6741ebb))

* notebooks: create general notebook for debugging ([`9df7b73`](https://github.com/bhklab/readii/commit/9df7b734a0ff6a871cccb593a486b91eb661af6b))

* notebooks: working on improving efficiency of negative control generation ([`bccb4f5`](https://github.com/bhklab/readii/commit/bccb4f5676df90a690e6846e5f04849e512b8884))


## v1.4.4 (2024-05-30)

### Bug Fixes

* fix: update docker image reference ([`91b3c05`](https://github.com/bhklab/readii/commit/91b3c057507e316df375a5fab34428cc47622922))


## v1.4.3 (2024-05-30)

### Bug Fixes

* fix: force build ([`45cab79`](https://github.com/bhklab/readii/commit/45cab79004e661b955157d7c4284351d532d50b4))

### Chores

* chore: update dependencies and workflow for continuous deployment ([`d400520`](https://github.com/bhklab/readii/commit/d4005204a85adacceea20cf00ceb22f51f684df4))


## v1.4.2 (2024-05-30)

### Bug Fixes

* fix: tag version in dockerfile ([`1b06ed8`](https://github.com/bhklab/readii/commit/1b06ed8a4c196f1e794c34717c700fff75a93f48))


## v1.4.1 (2024-05-30)

### Bug Fixes

* fix: add auto build docker ([`e1a58cd`](https://github.com/bhklab/readii/commit/e1a58cd94c2a2a99b0d71f9a536451b734f4f718))


## v1.4.0 (2024-05-29)

### Features

* feat(pipeline): added random seed command line argument for negative control creation ([`405fa74`](https://github.com/bhklab/readii/commit/405fa74f80c257c8e616d838dcc64b3865ac5bc9))

* feat(feature_extraction): added argument random seed for negative control creation ([`053d542`](https://github.com/bhklab/readii/commit/053d54266781863a2c5f285e3aec77a831aa1d28))

### Unknown

* Merge pull request #23 from bhklab/development_katy

Adding negative control to main pipeline and feature extraction functions ([`0afc838`](https://github.com/bhklab/readii/commit/0afc83833fcb80f2e158712bc1c8fd91e3b070e1))


## v1.3.4 (2024-05-16)

### Bug Fixes

* fix: poetry lock ([`0632d5a`](https://github.com/bhklab/readii/commit/0632d5ae3aa619387f2e3c8ff064c243dd5b3ee4))

* fix: pyradiomics original ([`4ab6aa7`](https://github.com/bhklab/readii/commit/4ab6aa7f7562a34c4ddf91a2697058fc796ee8a8))

* fix: pyradiomics original ([`9513427`](https://github.com/bhklab/readii/commit/9513427f2cf7a9d7a59adb250d8d1a76d5e45773))


## v1.3.3 (2024-05-16)

### Bug Fixes

* fix: install poetry ([`c1a905a`](https://github.com/bhklab/readii/commit/c1a905a7c3304d31e6edddb8332d98701b1ede18))


## v1.3.2 (2024-05-16)

### Bug Fixes

* fix: update lock ([`18054bd`](https://github.com/bhklab/readii/commit/18054bdadda30253b29eb06839dccaca356fbf1f))

* fix: no docker buils ([`e0a8e63`](https://github.com/bhklab/readii/commit/e0a8e63c584d0fcedbd5fcba42523d5d52a22a4d))


## v1.3.1 (2024-05-16)

### Bug Fixes

* fix: update readme with docker link

fix: update readme with docker link ([`4584af7`](https://github.com/bhklab/readii/commit/4584af76e908708e9af1edc4fba0622c8a0ad30c))

* fix: update readme with docker link ([`2f9a437`](https://github.com/bhklab/readii/commit/2f9a43707510154f207ff1b1ba31ddb879fb6e2d))


## v1.3.0 (2024-05-16)

### Bug Fixes

* fix(negative_controls): set random generated pixel value to int to work with SetPixel ([`8d9b071`](https://github.com/bhklab/readii/commit/8d9b0717428231ff8e8b96c5150953e487ce6038))

* fix(negative_controls): cast result from randNumGen.integers to int for sitk SetPixel function to fix type error ([`257c498`](https://github.com/bhklab/readii/commit/257c49873ebd73b0829b1b4d940e214c3a9192fe))

* fix(image_processing): correctedROIImage was assigned to unused variabel, changed to segImage ([`453402e`](https://github.com/bhklab/readii/commit/453402ed269cf7ec796a7337eae6fedabf07adc4))

* fix(test_negative_controls): makeRandomImage test was using incorrect function (shuffleImage) ([`143712a`](https://github.com/bhklab/readii/commit/143712a7885d957bbd63552a716b51ecbb4a9704))

### Build System

* build(poetry.lock): updated package versions ([`811b748`](https://github.com/bhklab/readii/commit/811b748184992b090fb96b0ec10ae5768cd6fa1d))

### Code Style

* style(feature_extraction): fix typo in randomizeImageFromDistributionSampling import ([`79dc539`](https://github.com/bhklab/readii/commit/79dc539c6802bc235347e16ba4025c39e3cfef4f))

* style(negative_controls): fix spelling of distribution in randomizeImageFromDistributionSampling ([`4a01f5c`](https://github.com/bhklab/readii/commit/4a01f5cb6eb448429d3cdac236ab06a3c6441282))

### Documentation

* docs(negative_controls): add random seed description to shuffleImage function header ([`df9a7d3`](https://github.com/bhklab/readii/commit/df9a7d3fa3cc9992a965e670a0474a19b9291cd2))

* docs(example.ipynb): update notebook to use med-imagetools CT DICOM loader ([`e6339b7`](https://github.com/bhklab/readii/commit/e6339b738f8cf05c04f12d5ae88b0e7baabc8685))

### Features

* feat(negative_controls): added random seed to all random functions and the apply negative control function ([`280b465`](https://github.com/bhklab/readii/commit/280b46578b6320dd8c9e66ee822dc0ffb7ac9d98))

* feat(negative_controls): add random seed to shuffleNonROI ([`a402ee5`](https://github.com/bhklab/readii/commit/a402ee57b9300558cd796bffe3ed3d8afa1e1654))

* feat(negative_controls): add random seed to shuffleROI ([`826b00d`](https://github.com/bhklab/readii/commit/826b00ddd92ae7fa1e4441426970066de66f8af4))

* feat(negative_controls): added random seed to shuffleImage function, now using numpy RNG and shuffle function ([`a2556ae`](https://github.com/bhklab/readii/commit/a2556aef0afe87f162bf3f6d12c572af23f9a9dc))

### Testing

* test(negative_controls): added tests for no roiLabel input for ROI and non-ROI negative control functions ([`c083878`](https://github.com/bhklab/readii/commit/c083878e86f8196ccbf2cf15eecb8b6c01f42754))

* test(negative_controls): removed redundant random pixel checks and added some checks for any change in the negative controls, updated some assertion failure messages ([`4ca434b`](https://github.com/bhklab/readii/commit/4ca434b34eebaf71064d3cc34f758d1bb6321556))

* test(negative_controls): update whole image pixel checks and remove random pixel checks in shuffleNonROI and makeRandomRoi ([`b970cbe`](https://github.com/bhklab/readii/commit/b970cbe72a2dc66262a3d3bdac8869a5dd160a59))

* test(negative_controls): update assertion comment in shuffle ROI ([`0c542f4`](https://github.com/bhklab/readii/commit/0c542f48ff07294e504713e51d6a171dbfb70d1c))

* test(negative_controls): fix the shuffle check that the same values exist in the new image in shuffleROI ([`6de291d`](https://github.com/bhklab/readii/commit/6de291d5c7595a31cfb22869784c6183ab4207ef))

* test(negative_controls): in makeRandomImage, added ROI voxel check, removed random pixel check as its covered by the randomSeed checks ([`17ca738`](https://github.com/bhklab/readii/commit/17ca7386daf7cb5d3437deb1d5dcca9b665b2d57))

* test(negative_controls): Added pixel check for centre of ROI, updated failed assertion message for randomSeed pixel checks ([`ed3bb17`](https://github.com/bhklab/readii/commit/ed3bb17768842339c5661fcfafebbd1c6efc786f))

* test(negative_controls): updated shuffle pixel check that values are the same as original ([`52dda33`](https://github.com/bhklab/readii/commit/52dda337b321b71b61922bbcb20363cea05c23eb))

* test(negative_controls): added random seed to rest of functions, changed conversion to pixels to include whole image not just region that's been altered ([`28db728`](https://github.com/bhklab/readii/commit/28db7280944c3e99dffa56e99fb297e27710d563))

* test(negative_controls): added random seed to shuffleROI and randomROI tests, updated negative control image variable to be clearer ([`e09c142`](https://github.com/bhklab/readii/commit/e09c14282427a2c854d06e25b69556b3ae6351ef))

* test(negative_controls): add random seed in shuffleROI test ([`d12ac25`](https://github.com/bhklab/readii/commit/d12ac25ba7cfb050017d365ef5d93825469e9a0c))

* test(negative_controls): updated nsclcCropped fixture to use getCroppedImages function ([`24dafff`](https://github.com/bhklab/readii/commit/24dafff25aeddd0bfded9b7dfbac4bf588ac7870))

* test(negative_controls): add random seed to make random image ([`6979ac6`](https://github.com/bhklab/readii/commit/6979ac6b72ac9a33aaa2f9178bf52ff711770478))

* test(negative_controls): add random seed to shuffle image test ([`c07c50e`](https://github.com/bhklab/readii/commit/c07c50e857d2dd3c1fff4a25d6f59f4074a2a784))

### Unknown

* Merge pull request #19 from bhklab/add_random_seed

Adding random seed to all negative controls for reproducible results ([`26d8cbc`](https://github.com/bhklab/readii/commit/26d8cbcd74aa0343634332de60dab3ca3b3a2cd6))


## v1.2.1 (2024-03-27)

### Bug Fixes

* fix: no development branch ([`e3349db`](https://github.com/bhklab/readii/commit/e3349dbc68dd3f8c4f72afe351148f8af2ef846f))

### Build System

* build: Update pytest command to run tests in parallel ([`e8f67b9`](https://github.com/bhklab/readii/commit/e8f67b9108f254431c0542a2812c674578db0794))

* build: update poetry lock ([`6999f20`](https://github.com/bhklab/readii/commit/6999f208f33132e53f6ba42037387ae41070bf07))

* build: Fix formatting in ci-cd.yml and add back unit tests. Rename jobs for better clarity ([`b4d49d5`](https://github.com/bhklab/readii/commit/b4d49d53fcccaa63e0e0d0b720da39f9f1dda3fb))

* build: add pytest-xdist for development parallel tests ([`d52a5a3`](https://github.com/bhklab/readii/commit/d52a5a3189cef9fc7599687f6dc1558378d87506))

### Code Style

* style(feature_extraction.py): changed some function call spacing ([`09331a3`](https://github.com/bhklab/readii/commit/09331a3d7f9b6459ab151b9b3611877c04f4d265))

### Refactoring

* refactor: format with black, explicit imports, and update type annotations ([`04bada5`](https://github.com/bhklab/readii/commit/04bada5a9d1933f840d647c4ef383329a6e9d2e7))

* refactor: Fixes, updates, formatting

refactor: Fixes, updates, formatting ([`998f299`](https://github.com/bhklab/readii/commit/998f299cfb3d29b95afde4f371508da2c6c142b6))

* refactor: format with black ([`07d04d8`](https://github.com/bhklab/readii/commit/07d04d8f1b8bacea29a896557971468446e22bf8))

* refactor: explicit imports from readii.metadata module for performance ([`f91afa4`](https://github.com/bhklab/readii/commit/f91afa43e63daeb06be8d9276c9607453d7fe71c))

* refactor: Refactor type check in test_radiomicFeatureExtraction ([`bc0d18d`](https://github.com/bhklab/readii/commit/bc0d18da89907ca82e30eb81fbed1ab1ae475cfe))

* refactor: Refactor saveDataframeCSV and matchCTtoSegmentation functions, add type hints, and improve error handling, format with black ([`16a83b9`](https://github.com/bhklab/readii/commit/16a83b9541d717f132f6a32afbeb89db02653c63))

* refactor: Update version variables in pyproject.toml ([`5776e5f`](https://github.com/bhklab/readii/commit/5776e5f0f618c3634d01fb86c685e012bc073a08))

* refactor: explicitly import all, nested import * can lead to performance issues ([`8054799`](https://github.com/bhklab/readii/commit/80547997d7d2c4c852a0f4f43b61d3c49ebe1f51))

* refactor: update type annotations. ([`c6ee885`](https://github.com/bhklab/readii/commit/c6ee885422df735b3230c5541936d3f71ab17f6c))

* refactor: update type annotations to handle optional parameters, format with black for readability, refactor applyNegativeControl function to raise AssertionErrror for optional baseROI, handle edge case and raise error if none of the nc_types. ([`11f0d92`](https://github.com/bhklab/readii/commit/11f0d92a3f86e1c1db328172d338b92b09654f46))

### Unknown

* Merge pull request #15 from bhklab/dockerfile

Refactor: Add dockerfile, fix some type errors, update type annotations, add some error-handling, formatting ([`20f8d54`](https://github.com/bhklab/readii/commit/20f8d543cfd27125ca21bb467acad13d556be284))

* fixed wrong docker repo ([`8ca1a93`](https://github.com/bhklab/readii/commit/8ca1a9349c7e0ac3bf13da572aa13d691d1cb56d))

* Merge branch 'dockerfile' of github.com:bhklab/readii into dockerfile ([`6bb042d`](https://github.com/bhklab/readii/commit/6bb042de6bf31a5869f0bfa016b7f38b229e5249))


## v1.2.0 (2024-03-15)

### Bug Fixes

* fix: wrong group in toml ([`b55baab`](https://github.com/bhklab/readii/commit/b55baabb4800e074f0f08684874947052ecb9195))

* fix: test builds and update toml to include this branch ([`af61beb`](https://github.com/bhklab/readii/commit/af61beba9a677a86695268a55bd2887138fb2c59))

* fix: test deployment ([`aa1dcb4`](https://github.com/bhklab/readii/commit/aa1dcb479720f8eec295071ad0b45aedaaf275d2))

### Features

* feat: adding dockerfile and gha to build and deploy ([`b7d6b73`](https://github.com/bhklab/readii/commit/b7d6b734ef6b955e5b61ff2d980a08893dc2dddb))

### Unknown

* Update ci-cd.yml and pyproject.toml ([`fa35141`](https://github.com/bhklab/readii/commit/fa35141d0d9b1772ac4d6242d942f4ad9c0061d3))


## v1.1.3 (2024-03-06)

### Bug Fixes

* fix(pipeline): need to exit when catching the no segmentation type error ([`bd1a93b`](https://github.com/bhklab/readii/commit/bd1a93bf0ac9d1104d3df2a46988b14b3401622b))

### Build System

* build: updating package versions ([`3f3a593`](https://github.com/bhklab/readii/commit/3f3a59358eaa7b5a81b12b8b45589d17f117df9c))

### Unknown

* Merge pull request #14 from bhklab/development_katy

Another fix for catching no segmentation type error ([`6e3e8fc`](https://github.com/bhklab/readii/commit/6e3e8fc8486334e7e3c1c438fc5ce757eb8a5585))


## v1.1.2 (2024-03-06)

### Documentation

* docs: update README with randomized sampled negative controls, add description of negative controls ([`eaff95d`](https://github.com/bhklab/readii/commit/eaff95df12d71af2dd7d69e59565cf00c3bc3e4e))

### Unknown

* Merge pull request #13 from bhklab/development_katy

fix (pipeline): catch error when there are no suitable segmentation types in the imgtools csv ([`f7f9904`](https://github.com/bhklab/readii/commit/f7f990465bef3f0b1124fb3052352a8f7e9e56af))

* fix (pipeline): catch error when there are no suitable segmentation types in the imgtools csv ([`6d475c9`](https://github.com/bhklab/readii/commit/6d475c978125496eaad62a2f49885da7fa964dc1))

* Merge pull request #12 from bhklab/development_mogtaba

Added ROI Name Quality Check  for Negative Controls ([`308ceaf`](https://github.com/bhklab/readii/commit/308ceafe882fb15fb0bc9a75638ab20da464411a))

* Added function to manually check for roi name if it is missing when calling negative control. Fixed output file checking ([`2810b59`](https://github.com/bhklab/readii/commit/2810b5971c39ed85b97f11d17f477d444a73e37e))

* Merge pull request #11 from bhklab/development_katy

docs: update README with randomized sampled negative controls, add de… ([`0c90846`](https://github.com/bhklab/readii/commit/0c908463559da5f8cd0a4a0fcc59eaa294ab4dd6))


## v1.1.1 (2024-02-08)

### Bug Fixes

* fix: update version number ([`3b90606`](https://github.com/bhklab/readii/commit/3b9060652fa39f8480691c5e5edc9e77c61131e9))

### Build System

* build: add pyarrow as dependency for pandas ([`0050dc1`](https://github.com/bhklab/readii/commit/0050dc156940aaab895a367c57307764d580c7d6))

* build: updated pyradiomics dependency tp 3.0.1a3 ([`d780b27`](https://github.com/bhklab/readii/commit/d780b27c7fcb4e05343f8575d63b3b5b4b0ae430))

* build: updated med-imagetools dependency ([`ed58b9c`](https://github.com/bhklab/readii/commit/ed58b9cfe726ac0d92d165c2e05bdb32753285a7))

* build: changed pyradiomics dependency to 3.0.1 as 3.1.0 has installation issues ([`9c89227`](https://github.com/bhklab/readii/commit/9c89227c7c97dadcacd94b7f450668c046c955a1))

* build: update dependencies versions ([`8b1af18`](https://github.com/bhklab/readii/commit/8b1af187f9e55dea34685b3a03c0abc80b318035))

### Unknown

* Merge pull request #10 from bhklab/development_katy

fix: update version number ([`2923f7a`](https://github.com/bhklab/readii/commit/2923f7aff3139c6eeae956fca1db7246d5d1f64a))

* fix version number ([`36e8ff8`](https://github.com/bhklab/readii/commit/36e8ff8f94389913bed1583bc87add3fb7bfdd92))

* patch: use pyradiomics 3.0.1a3 ([`98d5e91`](https://github.com/bhklab/readii/commit/98d5e9145ab8642ddb81c68e8fdf3e8b55f01eed))

* Merge pull request #9 from bhklab/development_katy

Development katy ([`0f1cc66`](https://github.com/bhklab/readii/commit/0f1cc665d27bd458a9d7f0f4e95577c4890b175b))

* bug(image_processing): force ROI voxel label to int to be compatible with pyradiomics 3.0.1a3 ([`38e7653`](https://github.com/bhklab/readii/commit/38e76532853573b1de204760a11f2833a235001a))


## v1.1.0 (2024-01-31)

### Bug Fixes

* fix(pipeline): fixed check for existing radiomic features file, had incorrect file name ([`1819d3d`](https://github.com/bhklab/readii/commit/1819d3d1e45132c195fed8e06c301005d05e18bf))

* fix(negative_controls): fixed function call for randomized_sample_full in applyNegativeControl ([`06a2f9c`](https://github.com/bhklab/readii/commit/06a2f9cf14be028ea46e8f29c371fbc7770791e6))

* fix(image_processing): moved crop to top of displayOverlay function to get correct centre slice index and array conversion happens after crop ([`c1037d9`](https://github.com/bhklab/readii/commit/c1037d9c7a353ab689b5688780a872d18184e2cd))

### Features

* feat(image_processing): made cropping CT and segmentation its own function ([`5202cc2`](https://github.com/bhklab/readii/commit/5202cc2113f392a0fce92c555bf58ff3085d3d97))

* feat(image_processing): add option to display CT and segmentation cropped to ROI ([`120524c`](https://github.com/bhklab/readii/commit/120524c17d89d3a2cee0c168b16243b385217cc2))

### Unknown

* Merge pull request #8 from bhklab/development_katy

Added display functions for CT and CT with segmentation overlaid
Fixed function call for randomized sample full image
Fixed check for existing radiomic features file ([`ba4a9fe`](https://github.com/bhklab/readii/commit/ba4a9fe1d80fad9a9f407ec0e36185af400584e9))

* Merge pull request #7 from bhklab/development_mogtaba

Fixed CTtoSegmentation merge issue and fixed negative control settings ([`7bbf3b7`](https://github.com/bhklab/readii/commit/7bbf3b7ff835df15ffea1e5cb561d2c1a15b168e))

* fixed merge between SEGs and CTs, in matchCTtoSegmentation ([`fc1dda1`](https://github.com/bhklab/readii/commit/fc1dda13ded85440c7d2b4ced3ccb86f9f028649))

* added new negative controls to --negative_control flag ([`9aaf76c`](https://github.com/bhklab/readii/commit/9aaf76c9c1f5edc968734fde5d03e86f2aa988c3))


## v1.0.0 (2024-01-26)

### Unknown

* Merge pull request #6 from bhklab/name_change

Name change from yarea to readii ([`2374af4`](https://github.com/bhklab/readii/commit/2374af46b6522ef617f6366a5b4d4d7e442a5d2c))

* Merge branch 'main' into name_change ([`480b596`](https://github.com/bhklab/readii/commit/480b59601294bd1a298fda026b6ebaecd570dfd1))

* Merge pull request #5 from bhklab/development_mogtaba

Created 3 new negative controls by sampling original image and tests ([`2f95cf7`](https://github.com/bhklab/readii/commit/2f95cf7d82c334e34611325c36ea0c1f0a881fbe))

* Created 3 new negative controls by sampling original image and added tests for them ([`ec3dd21`](https://github.com/bhklab/readii/commit/ec3dd21f3100ea22bcccd846020f55c052e204ad))

* merged changes ([`db63a6c`](https://github.com/bhklab/readii/commit/db63a6c766b1bd6e98dd10369336128038c2b7a1))


## v0.6.0 (2024-01-19)

### Breaking

* build: changed package name from YAREA to READII

BREAKING CHANGE: yarea name no longer used ([`3bcb4f9`](https://github.com/bhklab/readii/commit/3bcb4f9d9b1666f4fb3c3f66b4e4913358db25d7))

### Documentation

* docs(README): update package headline for READII acronym ([`1294d44`](https://github.com/bhklab/readii/commit/1294d44ed87a45567e6a957db77f9738817b37b4))

### Features

* feat(pipeline): change parallel input argument to be false by default ([`3f8c46a`](https://github.com/bhklab/readii/commit/3f8c46ade25b16a77cc1ee6175bda039b811561f))

### Unknown

* Merge pull request #4 from bhklab/development_katy

feat(pipeline): change parallel input argument to be false by default ([`8d0626d`](https://github.com/bhklab/readii/commit/8d0626d08acad7f9e2ca3d31560ea4d532f86e2e))

* Removed test that doesn't take into account shuffling edge case. ([`28ab19e`](https://github.com/bhklab/readii/commit/28ab19e652531095338935d9b6b655f7c3508d02))


## v0.5.0 (2024-01-17)

### Bug Fixes

* fix(image_processing): fixed remaining instances of imgArray variable ([`84de500`](https://github.com/bhklab/readii/commit/84de5003d65c8726d925108f087cdba3be9288ad))

* fix(image_processing): fixed image vs. imgArray variable mixup in displayImageSlice ([`c9ea3d6`](https://github.com/bhklab/readii/commit/c9ea3d6f1ae6637139c41651a3c66d133b6d6c5f))

### Build System

* build: updated dependency versions ([`44de606`](https://github.com/bhklab/readii/commit/44de60655fef29716ef5d4edbd6e1e18f8e508d1))

### Documentation

* docs(pipeline): indicate whether flags are true or false by default in help message of parallel and update ([`311dd5e`](https://github.com/bhklab/readii/commit/311dd5e4f946ba78caaf7c1f0d1ed6dceecd5dcb))

* docs(image_processing): wrote docstring for displayCTSegOverlay ([`2f69dab`](https://github.com/bhklab/readii/commit/2f69dab8f8d7b7b46f7fbe2175b356a4fb28baf7))

* docs: require python 3.9 in conda env setup ([`480b199`](https://github.com/bhklab/readii/commit/480b1997788be447a53a2699a952df076b7b5262))

### Features

* feat(image_processing): add function to display CT slice with segmentation overlaid ([`73342ef`](https://github.com/bhklab/readii/commit/73342efbd24757ac349124ba332dc26f89544ae9))

* feat(image_processing): add function to find center slice and coordinates of ROI in image ([`78d69b2`](https://github.com/bhklab/readii/commit/78d69b227ab1e2006ce46badd2b0a37384f45f40))

### Testing

* test(test_image_processing): added test for getROICenterCoords ([`8745fe7`](https://github.com/bhklab/readii/commit/8745fe752a27204eed7359aed4525c962481d2db))

### Unknown

* Merge pull request #3 from bhklab/development_katy

Added some new functions focused on displaying the CT with a segmentation overlaid and fixed a variable name in image_processing ([`04f42a4`](https://github.com/bhklab/readii/commit/04f42a40c7475499094e65ec55639a91b0da629f))

* Merge pull request #2 from bhklab/development_katy

docs: require python 3.9 in conda env setup ([`390d6e6`](https://github.com/bhklab/readii/commit/390d6e6f094968d0d19191484e14da16294e046e))


## v0.4.0 (2024-01-17)

### Documentation

* docs: add installation and usage details to README ([`4281620`](https://github.com/bhklab/readii/commit/4281620f5f791030a020cb4fe91b08318d63426b))

### Features

* feat: added command line example runs to notebook ([`48d8d40`](https://github.com/bhklab/readii/commit/48d8d40e24796491cb6491046b3f12f2424df128))

### Unknown

* add tests/output/ to gitignore to not commit output files ([`fa713ff`](https://github.com/bhklab/readii/commit/fa713ff38977b1d2758aae32bde5fa07f0500931))

* Merge branch 'main' of github.com:bhklab/yarea into main ([`1327e22`](https://github.com/bhklab/readii/commit/1327e22ab994212e24e4658313897791bef39c82))

* Fixed error with the path for CT and SEG files in the tests for negative controls ([`5ea6e2c`](https://github.com/bhklab/readii/commit/5ea6e2caa601f3aa3eefd806c1c09cdbef0c6e23))

* Fixed feature_extraction error where padSegToMatchCT function was being called incorrectly ([`82ad022`](https://github.com/bhklab/readii/commit/82ad0228bae60a5d800e15f77a9e6cad487e8c23))

* Add ci pass requirement back in ([`b678d4a`](https://github.com/bhklab/readii/commit/b678d4afb2c9818c07d0f8165f8b5baf3426e11c))

* Merge pull request #1 from bhklab/negative_control_tests

Created testing suite for negative controls and fixed errors in image_processing.py and negative_controls.py ([`f0fdd02`](https://github.com/bhklab/readii/commit/f0fdd028e167d78b371fc2ff73bff1328a271e54))

* merged conflicts ([`d78fb5f`](https://github.com/bhklab/readii/commit/d78fb5f101d3532b656a63f5134ac05d281f0bcf))

* Merge branch 'main' into negative_control_tests ([`c6ff12e`](https://github.com/bhklab/readii/commit/c6ff12ea94eb70691a71a9fb9fda7b655f272669))

* Finished testing suite for the negative controls ([`6d81739`](https://github.com/bhklab/readii/commit/6d81739841318c201508eb787f46d1024f78039b))

* Fixed issue with shuffleROI and shuffleNonROI, where some pixels with duplicate values were ignored ([`e812bcc`](https://github.com/bhklab/readii/commit/e812bccacaf5ad9f37d62811e6644dc2f6128159))

* Fixed error with wrong variable names, for CT folder path ([`302a284`](https://github.com/bhklab/readii/commit/302a284b904ceee539fee64b52b22c1e03f28fe1))

* Merge branch 'main' of github.com:bhklab/yarea into main ([`cee3c0f`](https://github.com/bhklab/readii/commit/cee3c0fe50b35d8ac491704d09d9a85e7ddbf2c4))


## v0.3.0 (2023-12-21)

### Bug Fixes

* fix(test_feature_extraction): fixed expected output path for radiomicFeatureExtraction ([`53c9db3`](https://github.com/bhklab/readii/commit/53c9db3bc31a35e332f9eeda35b82f42c84f5ab1))

* fix(image_processing): fixed usage of ctDirPath variable in padSegToMatchCT ([`892c8d7`](https://github.com/bhklab/readii/commit/892c8d7629595ce89f2893b004f6f7bc585bab21))

* fix: move size mismatch handling back to radiomicFeatureExtraction because image file paths are available in that function ([`ccbe852`](https://github.com/bhklab/readii/commit/ccbe8524fa69a2334b499512a541c3afa13b430a))

* fix(feature_extraction): moved error handling into singleRadiomicFeatureExtraction and added catch for wrong pyradiomics parameter file ([`41a3901`](https://github.com/bhklab/readii/commit/41a39018becde60091ffb113640e180a162d536f))

* fix: change radiomic features file output name ([`ea0b963`](https://github.com/bhklab/readii/commit/ea0b963c7c7caa0a39ab6149fa86d8783717bc32))

* fix(feature_extraction): add check for None in pyradiomics parameter file spot, use default if that's the case ([`5340f57`](https://github.com/bhklab/readii/commit/5340f57c8ab18818e6bb45cecda96fcb7aba4f5a))

* fix(yarea): renamed this file because it had import issues being named the same as the package ([`833c5b4`](https://github.com/bhklab/readii/commit/833c5b460140783d0292b7a1991bca7cbd0e5c64))

### Build System

* build: add publish to PyPI back in ([`e7f182e`](https://github.com/bhklab/readii/commit/e7f182e6b2da527ca9e0a747557bff1bc9dc0b6b))

* build: updated semantic release variables ([`5e24044`](https://github.com/bhklab/readii/commit/5e240446bc561cc34640a24d315edaf376cd244f))

* build: updated semantic release and added package build steps ([`5a51e07`](https://github.com/bhklab/readii/commit/5a51e078a8fbf3c0f14c7d0b429d14b830097142))

* build: remove publish to PyPI ([`f276b76`](https://github.com/bhklab/readii/commit/f276b767ae452eb7aceb702f607100e1c925c1c8))

### Code Style

* style(feature_extraction): changed ctFolderPath to ctDirPath for consistency ([`b7b452e`](https://github.com/bhklab/readii/commit/b7b452ea2d0c6f930cc727ec026b03de5d539121))

### Documentation

* docs(pipeline): fixed typo in data directory help message ([`7a19b5a`](https://github.com/bhklab/readii/commit/7a19b5a3d53ff24a6a800a7bcd75add2aff2d741))

### Features

* feat: add ability to run pipeline using poetry run ([`ced5e67`](https://github.com/bhklab/readii/commit/ced5e6771e3f7b688f2f394f0ec0f8b4ff92bf7a))

* feat(gitignore): ignore vscode directory with configurations ([`7e30be2`](https://github.com/bhklab/readii/commit/7e30be22e0a56c6f5f438e7ff51ebc9ba2b900f3))

* feat(pipeline): main pipeline function to run radiomic feature extraction ([`929573d`](https://github.com/bhklab/readii/commit/929573d50a22746fae29beceacd8d0169cd3dde3))

* feat(metadata): added check for csv type on imgFileListPath argument ([`ac09625`](https://github.com/bhklab/readii/commit/ac09625fd36622e5a0388ce8e4e74209ed4c9c4c))

* feat(metadata): made function to find the segmentation type from the list of image files ([`8dd4ddf`](https://github.com/bhklab/readii/commit/8dd4ddf858c47377d6bac0e9853282772d15dd43))

### Testing

* test(test_metadata): testing for getSegmentationType function ([`57768cf`](https://github.com/bhklab/readii/commit/57768cfe22fa0a7a3a59b65e25fe768848025ce0))

### Unknown

* remove files from tutorial ([`5afac9a`](https://github.com/bhklab/readii/commit/5afac9af90c7112c18acf2c3ce6f22a617c1cf86))

* updated version ([`3a063cf`](https://github.com/bhklab/readii/commit/3a063cf057fdfe3c056ca86af325f060c3c65cf3))


## v0.2.0 (2023-12-19)

### Bug Fixes

* fix: need to see test outputs for actions ([`6e95d0e`](https://github.com/bhklab/readii/commit/6e95d0e287a105c9f71d2f245fcdf10719913daf))

* fix: fixed default Pyradiomics parameter file path ([`84f16db`](https://github.com/bhklab/readii/commit/84f16db1d0032fa81dbf7b30422a74a0ec386984))

* fix: fixed inconsistencies and mistakes in variable names ([`7dd0d30`](https://github.com/bhklab/readii/commit/7dd0d3050916b4c2b1945ca772342f9599cc1b03))

* fix: incorrect indent in saveDataframeCSV ([`dd6d2f5`](https://github.com/bhklab/readii/commit/dd6d2f51bb55ae5bf5940b511862a7800c4a4fe1))

* fix: forgot to import pytest ([`6e978ca`](https://github.com/bhklab/readii/commit/6e978ca088971fe2ef80be629dcc6d7556c7cbd7))

* fix: fixed pyradiomics parameter file path and moved print statement of which ROI is processed back to radiomicFeatureExtraction ([`427eff7`](https://github.com/bhklab/readii/commit/427eff77663c66f919cfe239ae10b9080e4b0ef1))

* fix: missing pytest import and passing flattened SEG to alignImages ([`bab47e4`](https://github.com/bhklab/readii/commit/bab47e48a1f71d2ad8cde43ab9640c83b1337e00))

* fix: was missing pytest import ([`b38e7a4`](https://github.com/bhklab/readii/commit/b38e7a492a2bfd435ce21c4755268006cb226c44))

* fix: updated image file paths ([`588ba46`](https://github.com/bhklab/readii/commit/588ba465ce459c64a62857ca97830def18a8f4cf))

* fix: RTSTRUCT loader had incorrect variable for baseImageDirPath ([`6cfb08c`](https://github.com/bhklab/readii/commit/6cfb08cb52314931e98a71e3e9de5e0906debeb3))

### Build System

* build: add PSR as dev dependency ([`17cb2da`](https://github.com/bhklab/readii/commit/17cb2da3352995c9e716733c79fb1bb8f09de23f))

* build: add pyradiomics dependency ([`cb11289`](https://github.com/bhklab/readii/commit/cb11289446aad3d1f0b7d874af0b17189fce0959))

* build: add med-imagetools as a dependency ([`84aef0f`](https://github.com/bhklab/readii/commit/84aef0fe589a1177e8145e30f7b6df15b79de140))

### Features

* feat: changed outputFilePath to outputDirPath so output files can be standardized ([`d3ad8e8`](https://github.com/bhklab/readii/commit/d3ad8e8312dacb2315aace95722da777c3013e14))

* feat: changed input variable to outputDirPath to have consistent output file name ([`a0b3336`](https://github.com/bhklab/readii/commit/a0b33368c983b5f62993d46e0a06f295ac9951a4))

* feat: check that output file is a csv before starting any feature extraction ([`d2390f5`](https://github.com/bhklab/readii/commit/d2390f50c0bd0f14b13e1eda1729f20c0ca4f9b4))

* feat: ignore unit test output files ([`a3fd21e`](https://github.com/bhklab/readii/commit/a3fd21eaacc43d7d1b8571c71f91b4bde0e8a530))

* feat: added check for input not being a dataframe for saveDataframeCSV ([`69a0d84`](https://github.com/bhklab/readii/commit/69a0d84c1ab83487b059cf72d3d523d22cc37dc9))

* feat: function for extraction of radiomic features from a single CT and segmentation pair ([`ecb5d5b`](https://github.com/bhklab/readii/commit/ecb5d5bd4c5ba143622f4db9bfff350a5dc70e05))

* feat: added example pyradiomics config ([`2dee2eb`](https://github.com/bhklab/readii/commit/2dee2eb6ad5c355dec80ec8a72de7ff988077dbb))

* feat: function to run radiomic feature extraction, including negative control and parallel options ([`aeb6efd`](https://github.com/bhklab/readii/commit/aeb6efdcdea607738efe33437e443d5bc92d59c7))

* feat: add negative control generator functions ([`da6d9c0`](https://github.com/bhklab/readii/commit/da6d9c01275d399cb27191dc5eff21165107336b))

* feat: add function to match CTs and segmentations in medimagetools output and function to save out dataframe as csv ([`2f169e9`](https://github.com/bhklab/readii/commit/2f169e9eadae4f6a8fb73d34c48f03c7e652f991))

* feat: add seg label finder function ([`d575dee`](https://github.com/bhklab/readii/commit/d575dee223c8908eaedaa41312d361f113c9f768))

### Testing

* test: check output from radiomicFeatureExtraction ([`c525247`](https://github.com/bhklab/readii/commit/c525247f88029b70f17b1249fd2fdedfa6eb3ddf))

* test: test output saving for matchCTtoSegmentation ([`995726d`](https://github.com/bhklab/readii/commit/995726dbff3a8e6e2a74de3e0e12e9f35e11a7a6))

* test: updated test for radiomicFeatureExtraction to use default pyradiomics parameter file ([`617abbc`](https://github.com/bhklab/readii/commit/617abbcbf732433c08475652242830b6592fa321))

* test: added test for full radiomicFeatureExtraction function ([`ade890c`](https://github.com/bhklab/readii/commit/ade890cb2a1c8fd90f4fac433ade2c31e15f42a2))

* test: added incorrect object passed to saveDataframeCSV and fixed outputFilePath error test function call ([`281637b`](https://github.com/bhklab/readii/commit/281637b073dec5b1317a9d1bba627f036e552b64))

* test: test csv error in saveDataframeCSV ([`3a9929a`](https://github.com/bhklab/readii/commit/3a9929a53b67291b0da46b4f53a82515d4df364b))

* test: functions for singleRadiomicFeatureExtraction ([`37ec5d6`](https://github.com/bhklab/readii/commit/37ec5d6e587642895a5f59faf773b305ad02480e))

* test: started writing tests for radiomic feature extraction functions ([`cd31b86`](https://github.com/bhklab/readii/commit/cd31b86fda9bbca1c86111fcd9bd6ea0ff824daf))

* test: added tests for matchCTtoSegmentation function ([`c66d24c`](https://github.com/bhklab/readii/commit/c66d24c77910aaa8af515cb0ece7dcf283de7628))

* test: add getROIVoxelLabel test ([`2571cea`](https://github.com/bhklab/readii/commit/2571cea7c363f86716eb986588f746430502fb24))

* test: added image_processing unit tests ([`587eb2a`](https://github.com/bhklab/readii/commit/587eb2affeff25a4dfa59a2532029ec7989c9ecb))

* test: added image path fixtures and error check test ([`2b69fa1`](https://github.com/bhklab/readii/commit/2b69fa132e9f38868cfe895b6d29606ca6735d4f))

* test: add load segmentation module tests ([`6137f61`](https://github.com/bhklab/readii/commit/6137f6199628de184fc0b914871f0f1ee1059a07))

### Unknown

* data: changed naming convention for matchCTtoSeg output ([`0937fb5`](https://github.com/bhklab/readii/commit/0937fb538ec693eeef1212b18888ec682b2b1960))

* data: image metadata file for NSCLC_Radiogenomics, used in testing feature extraction ([`287349c`](https://github.com/bhklab/readii/commit/287349cfe0cbb33b0232aa865f29f81a2666b180))

* renamed file for consistency ([`39f969c`](https://github.com/bhklab/readii/commit/39f969c1b8f08fa8f1560b09bc380a270d2dc15a))

* data: imgtools output for test data for metadata tests ([`739c6e0`](https://github.com/bhklab/readii/commit/739c6e0a15fda507ed8a60cf76d03e462add5bac))

* Moved SEG example to named dataset directory ([`9f31b0c`](https://github.com/bhklab/readii/commit/9f31b0c42bf6d27e777be76a8638e77575d88002))

* updated dependencies ([`d42aec8`](https://github.com/bhklab/readii/commit/d42aec8b568d1cc745b644fe8aa3357cf314a2e5))

* Added test sample with RTSTRUCT segmentation ([`5124203`](https://github.com/bhklab/readii/commit/5124203b945b11ee64a659bd912b1661ac292835))

* Moved to named dataset folder ([`5077821`](https://github.com/bhklab/readii/commit/50778219cbffa6d86241a3e4bd28855606a24609))

* "feat: add example data and datasets module" ([`aaeded7`](https://github.com/bhklab/readii/commit/aaeded70258a8704df66994d0174a425050f8071))

* More renaming fixes ([`0776f25`](https://github.com/bhklab/readii/commit/0776f2564493315d54752ff6a0c17f3da6e20d88))

* test change in new repo ([`32aed17`](https://github.com/bhklab/readii/commit/32aed17a11048787d0b536210322918e9e5b3dc5))

* Renamed package to yarea ([`7519c43`](https://github.com/bhklab/readii/commit/7519c43e3950f907e6774a35095124ce4a2d630d))


## v0.1.0 (2023-11-23)

### Bug Fixes

* fix: correct conversion of sitk Image to array ([`34ddb65`](https://github.com/bhklab/readii/commit/34ddb6525983e69996671940e9f13f5107c69369))

* fix: updated segImagePath variable ([`166831c`](https://github.com/bhklab/readii/commit/166831ccfb0c37b4e057dde254cc387e6a016fc6))

### Build System

* build: added dev dependencies for docs ([`0e87a13`](https://github.com/bhklab/readii/commit/0e87a13807786bfb59aad4e5be9e9812033274fb))

* build: add pytest and pytest-cov as dev dependencies ([`152b825`](https://github.com/bhklab/readii/commit/152b825929a8c0982dd6d5210a14fb891d5b6396))

* build: remove upper bound on dependency versions ([`62ba9f8`](https://github.com/bhklab/readii/commit/62ba9f8f0ec84e8270083f7e82ffcecd30b8dd99))

* build: add loading and image processing dependencies ([`96fd62f`](https://github.com/bhklab/readii/commit/96fd62f9794c3a97d84d7b5e1c112c1f8a32cbd0))

### Documentation

* docs: updated example ([`794530e`](https://github.com/bhklab/readii/commit/794530e2309a448aea4e3775957dcd2e1f95f0ce))

* docs: updated docstrings for all functions ([`dbe6b84`](https://github.com/bhklab/readii/commit/dbe6b84ac9ecec6a5e5c2282d10ead56085de197))

### Features

* feat: added image processing functions ([`b0ac044`](https://github.com/bhklab/readii/commit/b0ac04443cdf39addc601678cea5f49f44f1f89f))

* feat: add image loader functions ([`73f67f5`](https://github.com/bhklab/readii/commit/73f67f55dbb59c5967f0d70cd7d7d146118e634e))

### Testing

* test: add unit test for loadDicomSITK ([`bef39f7`](https://github.com/bhklab/readii/commit/bef39f731363d1693f859ffbcdd6686540c1e98d))

### Unknown

* Changed segImagePath to be optional input ([`cd36ce8`](https://github.com/bhklab/readii/commit/cd36ce833d5ee2c4cdc031ca68df0d446b760a92))

* remove incorrect RTSTRUCT from tests ([`0350329`](https://github.com/bhklab/readii/commit/0350329703480f2511d114658618e9dc6880ad29))

* Added NSCLC_Radiogenomics sample for testing ([`8df5fbb`](https://github.com/bhklab/readii/commit/8df5fbb2ccca773d60d7a59588a6da56173abc1d))

* renamed for loader functions ([`8009a37`](https://github.com/bhklab/readii/commit/8009a374aaaa12fe1b875866724b93496e83d474))

* Added dependency imports ([`f4394dc`](https://github.com/bhklab/readii/commit/f4394dc69378bd85e142f1cb412eb2fac756c735))

* updated variable names to be consistent ([`d74a455`](https://github.com/bhklab/readii/commit/d74a455e5e8ceab8344e814dab76645685107623))

* initial package setup ([`18c743b`](https://github.com/bhklab/readii/commit/18c743be0ba4f15c121834ccf16f9e70bcc5ec09))
