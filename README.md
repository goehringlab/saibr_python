# SAIBR (python implementation)

[![CC BY 4.0][cc-by-shield]][cc-by]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests](https://github.com/goehringlab/saibr_python/actions/workflows/test.yaml/badge.svg)](https://github.com/goehringlab/saibr_python/actions/workflows/test.yaml)
[![PyPi version](https://badgen.net/pypi/v/saibr/)](https://pypi.org/project/saibr)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/goehringlab/saibr_python/HEAD?filepath=%2Fscripts/SAIBRdemonstration.ipynb)
[![Documentation Status](https://readthedocs.org/projects/saibr/badge/?version=latest)](https://saibr.readthedocs.io/en/latest/?badge=latest)


Python implementation of SAIBR: a simple, platform independent protocol for spectral autofluorescence correction

[Paper](https://journals.biologists.com/dev/article/149/14/dev200545/276004/SAIBR-a-simple-platform-independent-method-for)

[FIJI plugin](https://github.com/goehringlab/saibr_fiji_plugin)


## Tutorial notebook

As a first step, I would recommend checking out the [tutorial notebook](https://nbviewer.org/github/goehringlab/saibr_python/blob/master/scripts/SAIBRdemonstration.ipynb). This can be run in the cloud using Binder (please note that it may take several minutes to open the notebook):

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/goehringlab/saibr_python/HEAD?filepath=%2Fscripts/SAIBRdemonstration.ipynb)

To run locally, download the code and install the relevant requirements (requirements.txt) in a virtual environment.


## Install instructions

To explore further and incorporate into your own analysis pipelines, you can install the package from PyPI using pip:

    pip install saibr

If you want to make changes to the code you can download/clone this folder, navigate to it, and run:

    pip install -e .[dev]


## Citation

If you use this method as part of a publication, please cite the following reference: 

Nelio T. L. Rodrigues, Tom Bland, Joana Borrego-Pinto, KangBo Ng, Nisha Hirani, Ying Gu, Sherman Foo, Nathan W. Goehring; SAIBR: a simple, platform-independent method for spectral autofluorescence correction. Development 15 July 2022; 149 (14): dev200545. doi: https://doi.org/10.1242/dev.200545

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
