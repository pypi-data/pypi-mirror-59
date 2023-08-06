[![status](http://joss.theoj.org/papers/2ee6a3a3b1a4d8df1633f601bf2b0ffe/status.svg)](http://joss.theoj.org/papers/2ee6a3a3b1a4d8df1633f601bf2b0ffe)
[![CircleCI](https://circleci.com/gh/SebastianoF/bruker2nifti.svg?style=svg)](https://circleci.com/gh/SebastianoF/bruker2nifti)
[![coverage](https://github.com/SebastianoF/bruker2nifti/blob/master/coverage.svg)](https://github.com/SebastianoF/bruker2nifti/wiki/Local-testing-and-coverage-with-pytest-and-coveragerc)
[![PyPI version](https://badge.fury.io/py/bruker2nifti.svg)](https://badge.fury.io/py/bruker2nifti)

# Bruker2nifti

[Bruker2nifti](https://github.com/SebastianoF/bruker2nifti) is an open source medical image format converter from raw [Bruker](http://imaging.mrc-cbu.cam.ac.uk/imaging/FormatBruker)
ParaVision to [NifTi](https://nifti.nimh.nih.gov/nifti-1), without any intermediate step through the [DICOM](http://dicom.nema.org/standard.html) standard formats.

Bruker2nifti is a pip-installable pure Python tool provided with a Graphical User Interface and a Command Line Utility to access the conversion method.

### Before Getting Started

Since the release of ParaVision360v1.1, a NifTi format converter is natively embedded and would provide the long sought standard. Please consider this option before starting with bruker2nifti. 

### Getting Started

+ Requirements
    - Python 3 backward compatible with python 2.7
    - Libraries in [requirements.txt](https://github.com/SebastianoF/bruker2nifti/blob/master/requirements.txt).

+ Installation
    - Install the [latest stable release](https://github.com/SebastianoF/bruker2nifti/releases) with `pip install bruker2nifti`.
    - [Install the latest development version](https://github.com/SebastianoF/bruker2nifti/wiki/Installing-stable-version-and-development-version) with `pip install -e .`.

+ Real data examples
    - [Python-Ipython session](https://github.com/SebastianoF/bruker2nifti/wiki/Example:-use-bruker2nifti-in-a-python-(Ipython)-session).
    - [Command Line Interface (CLI)](https://github.com/SebastianoF/bruker2nifti/wiki/Example:-use-bruker2nifti-via-Command-Line-Interface).
    - [Graphical User Interface (GUI)](https://github.com/SebastianoF/bruker2nifti/wiki/Graphical-User-Interface-Examples).

## Accessing only the GUI with no Python knowledge required
+ [To access the Graphical User interface and convert some data with no python knowledge required](https://github.com/SebastianoF/bruker2nifti/wiki/Up-and-running-for-non-Python-developers).
+ [GUI instructions and real data examples](https://github.com/SebastianoF/bruker2nifti/wiki/Graphical-User-Interface-Examples).

![gui_example](https://github.com/SebastianoF/bruker2nifti/blob/master/screenshots/gui_version_101.jpg)

### API documentation, additional notes, examples and list of Bruker converter
+ [API documentation](http://bruker2nifti.readthedocs.io/en/latest/).
+ [Wiki documentation with additional notes and examples](https://github.com/SebastianoF/bruker2nifti/wiki).
+ [Links and list of available Bruker converter](https://github.com/SebastianoF/bruker2nifti/wiki/References).

### Code Testing

+ [Testing and Continuous integration with Pytest and Travis CI](https://github.com/SebastianoF/bruker2nifti/wiki/Code-Testing-and-Continuous-Integration-with-Pytest)
+ [Local testing and coverage with pytest and coveragerc](https://github.com/SebastianoF/bruker2nifti/wiki/Local-testing-and-coverage-with-pytest-and-coveragerc)
+ Tests are based on the benchmark dataset [Bruker2nifti_qa](https://gitlab.com/naveau/bruker2nifti_qa/tree/master) (thanks to Mikaël Naveau)

### Support and contributions

Please see the [contribution guideline](https://github.com/SebastianoF/bruker2nifti/blob/master/CONTRIBUTE.md) for bugs report,
feature requests and code style.

### Copyright, Licence and How to Cite

+ Copyright (c) 2017, Sebastiano Ferraris, University College London.
+ Bruker2nifti is provided as it is and copyrighted under [MIT License](https://github.com/SebastianoF/bruker2nifti/blob/master/LICENCE.txt).
+ To cite the code in your research please cite:

    + S. Ferraris, D. I. Shakir, J. Van Der Merwe, W. Gsell, J. Deprest, T. Vercauteren (2017), [Bruker2nifti: Magnetic Resonance Images converter from Bruker ParaVision to Nifti format](http://joss.theoj.org/papers/2ee6a3a3b1a4d8df1633f601bf2b0ffe),
    Journal of Open Source Software, 2(16), 354, [doi:10.21105/joss.00354](http://joss.theoj.org/papers/10.21105/joss.00354)

BibTeX entry:
```
@article{ferraris2017bruker2nifti,
  title={{Bruker2nifti: Magnetic Resonance Images converter from Bruker ParaVision to Nifti format}},
  author={Ferraris, Sebastiano and Shakir, Ismail Dzhoshkun and Van Der Merwe, Johannes and Gsell, Willy and Deprest, Jan and Vercauteren, Tom},
  journal={Journal Of Open Source Software},
  volume={2},
  number={16},
  pages={354},
  year={2017},
  publisher={Journal Of Open Source Software}
}
```

### Acknowledgements

+ This repository is developed within the [GIFT-surg research project](http://www.gift-surg.ac.uk).
+ Funding sources and authors list can be found in the [JOSS submission paper](https://github.com/SebastianoF/bruker2nifti/blob/master/paper/paper.md).
+ Thanks to
Bernard Siow (Centre for Advanced Biomedical Imaging, University College London),
Chris Rorden (McCausland Center for Brain Imaging, University of South Carolina)
and
Matthew Brett (Berkeley Brain Imaging Center).
