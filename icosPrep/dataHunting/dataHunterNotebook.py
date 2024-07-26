#!pip install jupyter_ui_poll
#!pip install loguru
#!pip install screeninfo
#!pip install git+https://github.com/ecederstrand/exchangelib
#! python --version
#!pip install -e .

from importlib import reload
import ipywidgets as wdg


if "dataHunter" not in dir():
    %run ./dataHunter
else:
    reload(dataHunter)
