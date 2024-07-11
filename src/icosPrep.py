#!/usr/bin/env python3

import sys
import argparse
from loguru import logger
from icosPrep.dataHunting.dataHunter import prepareCallToLumiaGUI
from icosPrep.dataPrep import prepData

def main():    
    p = argparse.ArgumentParser()
    p.add_argument('--start', dest='start', default=None, help="Start of the simulation in date+time ISO notation as in \'2018-08-31 00:18:00\'. Overwrites the value in the rc-file")
    p.add_argument('--end', dest='end', default=None, help="End of the simulation as in \'2018-12-31 23:59:59\'. Overwrites the value in the rc-file")
    p.add_argument('--ymf', dest='ymf', default=None,  help='yaml configuration file where the user plans his or her Lumia run: parameters, input files etc.')   
    p.add_argument('--noTkinter', '-n', action='store_true', default=False, help="Do not use tkinter (=> use ipywidgets)")
    p.add_argument('--verbosity', '-v', dest='verbosity', default='INFO')
    args, unknown = p.parse_known_args(sys.argv[1:])
    
    # Set the verbosity in the logger (loguru quirks ...)
    logger.remove()
    logger.add(sys.stderr, level=args.verbosity)
    
    USE_TKINTER=False # when called from lumiaGUInotebook.ipynb there are no commandline options
    if((args.start is not None) or (args.rcf is not None) or (args.ymf is not None)):
        USE_TKINTER=True # called as a notebook, not from the commandline
    if(args.noTkinter):
        USE_TKINTER=False
    if(args.rcf is None):
        if(args.ymf is None):
            ymlFile=None
        else:
            ymlFile = args.ymf
    else:            
        ymlFile = args.rcf
    
    
    # Call the main data hunting method
    ymlFile=prepareCallToLumiaGUI(ymlFile,  USE_TKINTER,  USE_TKINTER, args)
    
    # The ymlFile has been updated or execution has been aborted before getting to this point in the script....
    prepData(ymlFile)
    
