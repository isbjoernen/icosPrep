


icosPrep

This package is intended for scientific use. It discovers data on the icos.eu carbon portal and prepares it for use in an atmospheric inversion model (e.g. LUMIA)
It provides a graphical user interface for setting up the configuration file for LUMIA. This includes an interface to the ICOS carbon portal and the
interactive selection of observational data from the ICOS carbon portal icos.eu
icosPrep has been developped further from lumiaGUI and the lumiaDA branch of LUMIA [https://github.com/lumia-dev/lumia/tree/LumiaDA](https://github.com/lumia-dev/lumia/tree/LumiaDA)
project. Its aim is to prepare all input data in an offline archive though with full documentatation of all persistent identifiers such that the data
could be re-created at any moment

We recommend getting the latest commit from [github](https://github.com/isbjoernen/icosPrep.git):

```bash
git clone --branch master https://github.com/isbjoernen/icosPrep.git
```

# Folder structure

The folder structure of icosPrep is the following:

- "the _dataHunting_ folder contains what used to be lumiaGUI. It queries the ICOS carbon portal for files matching the user's selections"
- the _docs_ folder contains a more extensive documentation
- the _dataPrep_ folder contains the scripts necessary to download and combine the data found on the icos portal in the previous step.
- "the _auxiliary_ folder's sole file outputEraser.py is a standalone module (for deleting obsolete data - use with care)"
- the _utils_ folder contains some general routines that can be called from anywhere in the code.


# Installation

icosPep is written in python, and depends on many other scientific packages. We recommend using in a [miniconda](https://docs.conda.io/projects/miniconda/en/latest/) virtual environment, with at least the `cartopy` package installed:
```bash
# Create a conda environment for your LUMIA project (change `my_proj` by the name you want to give it)
conda create -n my_proj cartopy

# Activate the environment:
conda activate my_proj

# Clone lumia from its git repository (change `my_folder` by the name of the folder you want LUMIA to be installed in. The folder should not exist before)
git clone --branch master https://github.com/lumia-dev/lumia.git my_folder

# Install the LUMIA python library inside your virtual environment (replace `my_folder` by the name of the folder where you have cloned LUMIA in).
pip install -e my_folder
```

???+ Warning "Dos and Don'ts"
    * Do get familiar with how python packages should be installed [https://docs.python.org/dev/installing/index.html](https://docs.python.org/dev/installing/index.html)
    * Do get familiar with how conda environments work:
        - [conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
        - [conda cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
    * Don't try to use the _Makefile_ directly (but you can look at it, it contains a shortened version of this documentation).

# Testing the installation

Once you have installed `lumia` in your python environment (i.e. once you have gone through the [installation instructions above](#1.-recommended-installation)), the `lumia` module will be accessible on your system. Try for example:
```bash
conda activate my_proj  # Make sure you are in the right python environment!
cd /tmp                 # Move to another folder, basically anywhere where your lumia files are not
python -m lumia         # Run python with the `lumia` module
```

This should produce an error such as:
```bash
/home/myself/miniconda3/envs/my_proj/bin/python: No module named lumia.__main__; 'lumia' is a package and cannot be directly executed
```

This is good! it means that python has found lumia (but doesn't know what to do with it, that's another issue).

If you get instead an error such as:
```bash
/usr/bin/python3: No module named lumia
```
This means that python cannot find the `lumia` module: either you are not within the right python environment (read the [conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) if you are not familiar with it), or that another error happened during the installation of `lumia` (did you use the `pip install -e /path/to/lumia` as instructed above? did that return an error (maybe some dependency could not be installed?)).

# Recommended workflow

Contents to be written


# Documentation summary

This package is intended for scientific use. It discovers data on the icos.eu carbon portal and prepares it for use in an atmospheric inversion model (e.g. LUMIA)
It provides a graphical user interface for setting up the configuration file for LUMIA.

