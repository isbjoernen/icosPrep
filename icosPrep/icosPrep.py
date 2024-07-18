#!/usr/bin/env python3

from os import path, system
import sys
import argparse
from pathlib import Path
from loguru import logger

from dataPrep.prepData import prepData
#from dataHunting.dataHunter import prepareCallToLumiaGUI

#def main():    
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

import icosPrep
script_directory=path.dirname(icosPrep.__file__)
sCmd='python '+str(script_directory)+'/dataHunting/dataHunter.py '

'''
USE_TKINTER=False # when called from lumiaGUInotebook.ipynb there are no commandline options
if((args.start is not None) or (args.ymf is not None)):
    USE_TKINTER=True # called from the commandline
'''    
if(args.noTkinter):
    # USE_TKINTER=False
    sCmd=sCmd+' --noTkinter '
if(args.verbosity):
    sCmd=sCmd+' --verbosity='+str(args.verbosity)
if(args.ymf is None):
    ymlFile=None
else:
    ymlFile = args.ymf
    sCmd=sCmd+' --ymf='+str(ymlFile)
if not(args.start is None):
    sCmd=sCmd+' --start='+str(args.start)
if not(args.end is None):
    sCmd=sCmd+' --end='+str(args.end)
    
script_directory=Path(script_directory)
packageRootDir=script_directory.parent  # where .git directory lives.....
sCmd=sCmd+' --rootDir='+str(packageRootDir)

# Call the main data hunting method
#ymlFile=prepareCallToLumiaGUI(ymlFile,  USE_TKINTER,  packageRootDir,  args)
try:
    logger.info(sCmd)
    system(sCmd)
except:
    sys.exit('Abort. Call to dataHunter.py failed') 
        
# The ymlFile has been updated or execution has been aborted before getting to this point in the script....
prepData(ymlFile)

