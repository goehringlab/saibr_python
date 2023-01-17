from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='saibr',
    version='0.1.1',
    license="CC BY 4.0",
    author='Tom Bland',
    author_email='tom_bland@hotmail.co.uk',
    packages=find_packages(),
    url='https://github.com/goehringlab/saibr_python',
    install_requires=['numpy',
                      'matplotlib',
                      'scipy',
                      'ipywidgets',
                      'scikit-learn',
                      'scikit-image',
                      'jupyter',
                      'opencv-python'],
    description='Python implementation of SAIBR: a tool for performing spectral autofluorescence correction on biological images',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
