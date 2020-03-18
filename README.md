# EEG-BCI

## Instalation

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