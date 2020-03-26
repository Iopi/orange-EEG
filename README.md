Orange3-Eeg
===========

[![docs](https://img.shields.io/badge/python-passing-green.svg)](https://orange3-eeg.readthedocs.io/en/latest//)
[![Python 3.6](https://img.shields.io/badge/python-%3E=3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![mne](https://img.shields.io/badge/mne-0.17.1-blueviolet.svg)](https://mne.tools/0.17/install_mne_python.html)
[![AnyQt](https://img.shields.io/badge/AnyQt--green.svg)](https://pypi.org/project/AnyQt/)
[![PyQt5](https://img.shields.io/badge/PyQt5--green.svg)](https://pypi.org/project/PyQt5/)
[![numpy](https://img.shields.io/badge/numpy--blue.svg)](https://numpy.org/)
[![pylsl](https://img.shields.io/badge/pylsl--blue.svg)](https://pypi.org/project/pylsl/)
[![PyWavelets](https://img.shields.io/badge/pywt--blue.svg)](https://pywavelets.readthedocs.io/en/latest/install.html)

Orange add-on containing widgets that work with EEG data"

Package documentation: https://orange3-eeg.readthedocs.io/en/latest/

## Instalation

Firstly install Orange3 version 3.23.1. The process can be found here - [Orange3 Download](https://orange.biolab.si/download/#windows).

After successfully installing Orange3, you can install the Orange3-Eeg add-on package.

To install the add-on, run
    
    pip install .

To install the add-on, but keep the code in development directory, run

    pip install -e .
    
this will make it so that Orange recognizes the package, and when changes are made
to the source code it will recognize them too.

## Usage
After the installation, Orange should now be tracking the package, simply run

    python -m Orange.canvas
    
the EEG category should show in the left menu in the orange application.