# CHANGELOG



## v0.3.0 (2023-12-21)

### Build

* build: updated semantic release variables ([`5e24044`](https://github.com/bhklab/yarea/commit/5e240446bc561cc34640a24d315edaf376cd244f))

* build: updated semantic release and added package build steps ([`5a51e07`](https://github.com/bhklab/yarea/commit/5a51e078a8fbf3c0f14c7d0b429d14b830097142))

* build: remove publish to PyPI ([`f276b76`](https://github.com/bhklab/yarea/commit/f276b767ae452eb7aceb702f607100e1c925c1c8))

### Documentation

* docs(pipeline): fixed typo in data directory help message ([`7a19b5a`](https://github.com/bhklab/yarea/commit/7a19b5a3d53ff24a6a800a7bcd75add2aff2d741))

### Feature

* feat: add ability to run pipeline using poetry run ([`ced5e67`](https://github.com/bhklab/yarea/commit/ced5e6771e3f7b688f2f394f0ec0f8b4ff92bf7a))

* feat(gitignore): ignore vscode directory with configurations ([`7e30be2`](https://github.com/bhklab/yarea/commit/7e30be22e0a56c6f5f438e7ff51ebc9ba2b900f3))

* feat(pipeline): main pipeline function to run radiomic feature extraction ([`929573d`](https://github.com/bhklab/yarea/commit/929573d50a22746fae29beceacd8d0169cd3dde3))

* feat(metadata): added check for csv type on imgFileListPath argument ([`ac09625`](https://github.com/bhklab/yarea/commit/ac09625fd36622e5a0388ce8e4e74209ed4c9c4c))

* feat(metadata): made function to find the segmentation type from the list of image files ([`8dd4ddf`](https://github.com/bhklab/yarea/commit/8dd4ddf858c47377d6bac0e9853282772d15dd43))

### Fix

* fix(test_feature_extraction): fixed expected output path for radiomicFeatureExtraction ([`53c9db3`](https://github.com/bhklab/yarea/commit/53c9db3bc31a35e332f9eeda35b82f42c84f5ab1))

* fix(image_processing): fixed usage of ctDirPath variable in padSegToMatchCT ([`892c8d7`](https://github.com/bhklab/yarea/commit/892c8d7629595ce89f2893b004f6f7bc585bab21))

* fix: move size mismatch handling back to radiomicFeatureExtraction because image file paths are available in that function ([`ccbe852`](https://github.com/bhklab/yarea/commit/ccbe8524fa69a2334b499512a541c3afa13b430a))

* fix(feature_extraction): moved error handling into singleRadiomicFeatureExtraction and added catch for wrong pyradiomics parameter file ([`41a3901`](https://github.com/bhklab/yarea/commit/41a39018becde60091ffb113640e180a162d536f))

* fix: change radiomic features file output name ([`ea0b963`](https://github.com/bhklab/yarea/commit/ea0b963c7c7caa0a39ab6149fa86d8783717bc32))

* fix(feature_extraction): add check for None in pyradiomics parameter file spot, use default if that&#39;s the case ([`5340f57`](https://github.com/bhklab/yarea/commit/5340f57c8ab18818e6bb45cecda96fcb7aba4f5a))

* fix(yarea): renamed this file because it had import issues being named the same as the package ([`833c5b4`](https://github.com/bhklab/yarea/commit/833c5b460140783d0292b7a1991bca7cbd0e5c64))

### Style

* style(feature_extraction): changed ctFolderPath to ctDirPath for consistency ([`b7b452e`](https://github.com/bhklab/yarea/commit/b7b452ea2d0c6f930cc727ec026b03de5d539121))

### Test

* test(test_metadata): testing for getSegmentationType function ([`57768cf`](https://github.com/bhklab/yarea/commit/57768cfe22fa0a7a3a59b65e25fe768848025ce0))

### Unknown

* remove files from tutorial ([`5afac9a`](https://github.com/bhklab/yarea/commit/5afac9af90c7112c18acf2c3ce6f22a617c1cf86))

* updated version ([`3a063cf`](https://github.com/bhklab/yarea/commit/3a063cf057fdfe3c056ca86af325f060c3c65cf3))


## v0.2.0 (2023-12-20)

### Build

* build: add PSR as dev dependency ([`17cb2da`](https://github.com/bhklab/yarea/commit/17cb2da3352995c9e716733c79fb1bb8f09de23f))

* build: add pyradiomics dependency ([`cb11289`](https://github.com/bhklab/yarea/commit/cb11289446aad3d1f0b7d874af0b17189fce0959))

* build: add med-imagetools as a dependency ([`84aef0f`](https://github.com/bhklab/yarea/commit/84aef0fe589a1177e8145e30f7b6df15b79de140))

### Feature

* feat: changed outputFilePath to outputDirPath so output files can be standardized ([`d3ad8e8`](https://github.com/bhklab/yarea/commit/d3ad8e8312dacb2315aace95722da777c3013e14))

* feat: changed input variable to outputDirPath to have consistent output file name ([`a0b3336`](https://github.com/bhklab/yarea/commit/a0b33368c983b5f62993d46e0a06f295ac9951a4))

* feat: check that output file is a csv before starting any feature extraction ([`d2390f5`](https://github.com/bhklab/yarea/commit/d2390f50c0bd0f14b13e1eda1729f20c0ca4f9b4))

* feat: ignore unit test output files ([`a3fd21e`](https://github.com/bhklab/yarea/commit/a3fd21eaacc43d7d1b8571c71f91b4bde0e8a530))

* feat: added check for input not being a dataframe for saveDataframeCSV ([`69a0d84`](https://github.com/bhklab/yarea/commit/69a0d84c1ab83487b059cf72d3d523d22cc37dc9))

* feat: function for extraction of radiomic features from a single CT and segmentation pair ([`ecb5d5b`](https://github.com/bhklab/yarea/commit/ecb5d5bd4c5ba143622f4db9bfff350a5dc70e05))

* feat: added example pyradiomics config ([`2dee2eb`](https://github.com/bhklab/yarea/commit/2dee2eb6ad5c355dec80ec8a72de7ff988077dbb))

* feat: function to run radiomic feature extraction, including negative control and parallel options ([`aeb6efd`](https://github.com/bhklab/yarea/commit/aeb6efdcdea607738efe33437e443d5bc92d59c7))

* feat: add negative control generator functions ([`da6d9c0`](https://github.com/bhklab/yarea/commit/da6d9c01275d399cb27191dc5eff21165107336b))

* feat: add function to match CTs and segmentations in medimagetools output and function to save out dataframe as csv ([`2f169e9`](https://github.com/bhklab/yarea/commit/2f169e9eadae4f6a8fb73d34c48f03c7e652f991))

* feat: add seg label finder function ([`d575dee`](https://github.com/bhklab/yarea/commit/d575dee223c8908eaedaa41312d361f113c9f768))

### Fix

* fix: need to see test outputs for actions ([`6e95d0e`](https://github.com/bhklab/yarea/commit/6e95d0e287a105c9f71d2f245fcdf10719913daf))

* fix: fixed default Pyradiomics parameter file path ([`84f16db`](https://github.com/bhklab/yarea/commit/84f16db1d0032fa81dbf7b30422a74a0ec386984))

* fix: fixed inconsistencies and mistakes in variable names ([`7dd0d30`](https://github.com/bhklab/yarea/commit/7dd0d3050916b4c2b1945ca772342f9599cc1b03))

* fix: incorrect indent in saveDataframeCSV ([`dd6d2f5`](https://github.com/bhklab/yarea/commit/dd6d2f51bb55ae5bf5940b511862a7800c4a4fe1))

* fix: forgot to import pytest ([`6e978ca`](https://github.com/bhklab/yarea/commit/6e978ca088971fe2ef80be629dcc6d7556c7cbd7))

* fix: fixed pyradiomics parameter file path and moved print statement of which ROI is processed back to radiomicFeatureExtraction ([`427eff7`](https://github.com/bhklab/yarea/commit/427eff77663c66f919cfe239ae10b9080e4b0ef1))

* fix: missing pytest import and passing flattened SEG to alignImages ([`bab47e4`](https://github.com/bhklab/yarea/commit/bab47e48a1f71d2ad8cde43ab9640c83b1337e00))

* fix: was missing pytest import ([`b38e7a4`](https://github.com/bhklab/yarea/commit/b38e7a492a2bfd435ce21c4755268006cb226c44))

* fix: updated image file paths ([`588ba46`](https://github.com/bhklab/yarea/commit/588ba465ce459c64a62857ca97830def18a8f4cf))

* fix: RTSTRUCT loader had incorrect variable for baseImageDirPath ([`6cfb08c`](https://github.com/bhklab/yarea/commit/6cfb08cb52314931e98a71e3e9de5e0906debeb3))

### Test

* test: check output from radiomicFeatureExtraction ([`c525247`](https://github.com/bhklab/yarea/commit/c525247f88029b70f17b1249fd2fdedfa6eb3ddf))

* test: test output saving for matchCTtoSegmentation ([`995726d`](https://github.com/bhklab/yarea/commit/995726dbff3a8e6e2a74de3e0e12e9f35e11a7a6))

* test: updated test for radiomicFeatureExtraction to use default pyradiomics parameter file ([`617abbc`](https://github.com/bhklab/yarea/commit/617abbcbf732433c08475652242830b6592fa321))

* test: added test for full radiomicFeatureExtraction function ([`ade890c`](https://github.com/bhklab/yarea/commit/ade890cb2a1c8fd90f4fac433ade2c31e15f42a2))

* test: added incorrect object passed to saveDataframeCSV and fixed outputFilePath error test function call ([`281637b`](https://github.com/bhklab/yarea/commit/281637b073dec5b1317a9d1bba627f036e552b64))

* test: test csv error in saveDataframeCSV ([`3a9929a`](https://github.com/bhklab/yarea/commit/3a9929a53b67291b0da46b4f53a82515d4df364b))

* test: functions for singleRadiomicFeatureExtraction ([`37ec5d6`](https://github.com/bhklab/yarea/commit/37ec5d6e587642895a5f59faf773b305ad02480e))

* test: started writing tests for radiomic feature extraction functions ([`cd31b86`](https://github.com/bhklab/yarea/commit/cd31b86fda9bbca1c86111fcd9bd6ea0ff824daf))

* test: added tests for matchCTtoSegmentation function ([`c66d24c`](https://github.com/bhklab/yarea/commit/c66d24c77910aaa8af515cb0ece7dcf283de7628))

* test: add getROIVoxelLabel test ([`2571cea`](https://github.com/bhklab/yarea/commit/2571cea7c363f86716eb986588f746430502fb24))

* test: added image_processing unit tests ([`587eb2a`](https://github.com/bhklab/yarea/commit/587eb2affeff25a4dfa59a2532029ec7989c9ecb))

* test: added image path fixtures and error check test ([`2b69fa1`](https://github.com/bhklab/yarea/commit/2b69fa132e9f38868cfe895b6d29606ca6735d4f))

* test: add load segmentation module tests ([`6137f61`](https://github.com/bhklab/yarea/commit/6137f6199628de184fc0b914871f0f1ee1059a07))

### Unknown

* data: changed naming convention for matchCTtoSeg output ([`0937fb5`](https://github.com/bhklab/yarea/commit/0937fb538ec693eeef1212b18888ec682b2b1960))

* data: image metadata file for NSCLC_Radiogenomics, used in testing feature extraction ([`287349c`](https://github.com/bhklab/yarea/commit/287349cfe0cbb33b0232aa865f29f81a2666b180))

* renamed file for consistency ([`39f969c`](https://github.com/bhklab/yarea/commit/39f969c1b8f08fa8f1560b09bc380a270d2dc15a))

* data: imgtools output for test data for metadata tests ([`739c6e0`](https://github.com/bhklab/yarea/commit/739c6e0a15fda507ed8a60cf76d03e462add5bac))

* Moved SEG example to named dataset directory ([`9f31b0c`](https://github.com/bhklab/yarea/commit/9f31b0c42bf6d27e777be76a8638e77575d88002))

* updated dependencies ([`d42aec8`](https://github.com/bhklab/yarea/commit/d42aec8b568d1cc745b644fe8aa3357cf314a2e5))

* Added test sample with RTSTRUCT segmentation ([`5124203`](https://github.com/bhklab/yarea/commit/5124203b945b11ee64a659bd912b1661ac292835))

* Moved to named dataset folder ([`5077821`](https://github.com/bhklab/yarea/commit/50778219cbffa6d86241a3e4bd28855606a24609))

* &#34;feat: add example data and datasets module&#34; ([`aaeded7`](https://github.com/bhklab/yarea/commit/aaeded70258a8704df66994d0174a425050f8071))

* More renaming fixes ([`0776f25`](https://github.com/bhklab/yarea/commit/0776f2564493315d54752ff6a0c17f3da6e20d88))

* test change in new repo ([`32aed17`](https://github.com/bhklab/yarea/commit/32aed17a11048787d0b536210322918e9e5b3dc5))

* Renamed package to yarea ([`7519c43`](https://github.com/bhklab/yarea/commit/7519c43e3950f907e6774a35095124ce4a2d630d))


## v0.1.0 (2023-11-24)

### Build

* build: added dev dependencies for docs ([`0e87a13`](https://github.com/bhklab/yarea/commit/0e87a13807786bfb59aad4e5be9e9812033274fb))

* build: add pytest and pytest-cov as dev dependencies ([`152b825`](https://github.com/bhklab/yarea/commit/152b825929a8c0982dd6d5210a14fb891d5b6396))

* build: remove upper bound on dependency versions ([`62ba9f8`](https://github.com/bhklab/yarea/commit/62ba9f8f0ec84e8270083f7e82ffcecd30b8dd99))

* build: add loading and image processing dependencies ([`96fd62f`](https://github.com/bhklab/yarea/commit/96fd62f9794c3a97d84d7b5e1c112c1f8a32cbd0))

### Documentation

* docs: updated example ([`794530e`](https://github.com/bhklab/yarea/commit/794530e2309a448aea4e3775957dcd2e1f95f0ce))

* docs: updated docstrings for all functions ([`dbe6b84`](https://github.com/bhklab/yarea/commit/dbe6b84ac9ecec6a5e5c2282d10ead56085de197))

### Feature

* feat: added image processing functions ([`b0ac044`](https://github.com/bhklab/yarea/commit/b0ac04443cdf39addc601678cea5f49f44f1f89f))

* feat: add image loader functions ([`73f67f5`](https://github.com/bhklab/yarea/commit/73f67f55dbb59c5967f0d70cd7d7d146118e634e))

### Fix

* fix: correct conversion of sitk Image to array ([`34ddb65`](https://github.com/bhklab/yarea/commit/34ddb6525983e69996671940e9f13f5107c69369))

* fix: updated segImagePath variable ([`166831c`](https://github.com/bhklab/yarea/commit/166831ccfb0c37b4e057dde254cc387e6a016fc6))

### Test

* test: add unit test for loadDicomSITK ([`bef39f7`](https://github.com/bhklab/yarea/commit/bef39f731363d1693f859ffbcdd6686540c1e98d))

### Unknown

* Changed segImagePath to be optional input ([`cd36ce8`](https://github.com/bhklab/yarea/commit/cd36ce833d5ee2c4cdc031ca68df0d446b760a92))

* remove incorrect RTSTRUCT from tests ([`0350329`](https://github.com/bhklab/yarea/commit/0350329703480f2511d114658618e9dc6880ad29))

* Added NSCLC_Radiogenomics sample for testing ([`8df5fbb`](https://github.com/bhklab/yarea/commit/8df5fbb2ccca773d60d7a59588a6da56173abc1d))

* renamed for loader functions ([`8009a37`](https://github.com/bhklab/yarea/commit/8009a374aaaa12fe1b875866724b93496e83d474))

* Added dependency imports ([`f4394dc`](https://github.com/bhklab/yarea/commit/f4394dc69378bd85e142f1cb412eb2fac756c735))

* updated variable names to be consistent ([`d74a455`](https://github.com/bhklab/yarea/commit/d74a455e5e8ceab8344e814dab76645685107623))

* initial package setup ([`18c743b`](https://github.com/bhklab/yarea/commit/18c743be0ba4f15c121834ccf16f9e70bcc5ec09))
