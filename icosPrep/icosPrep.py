#!/usr/bin/env python3

from os import path, system
import sys
import argparse
from pathlib import Path
from loguru import logger
#from dataHunting.dataHunter import prepareCallToLumiaGUI

# icosPrepInstallDir=path.dirname(__file__)

def main():    
    p = argparse.ArgumentParser()
    p.add_argument('--start', dest='start', default=None, help="Start of the simulation in date+time ISO notation as in \'2018-08-31 00:18:00\'. Overwrites the value in the rc-file")
    p.add_argument('--end', dest='end', default=None, help="End of the simulation as in \'2018-12-31 23:59:59\'. Overwrites the value in the rc-file")
    p.add_argument('--machine', '-m', default='UNKNOWN', help='Name of the section of the yaml file to be used as "machine". It should contain the machine-specific settings (paths, number of CPUs, paths to secrets, etc.)')
    p.add_argument('--ymf', dest='ymf', default=None,  help='Required. Yaml configuration file where the user configues his or her Lumia run: parameters, input files etc.')   
    p.add_argument('--noTkinter', '-n', action='store_true', default=False, help="Do not use tkinter (=> use ipywidgets)")
    p.add_argument('--verbosity', '-v', dest='verbosity', default='INFO')
    args, unknown = p.parse_known_args(sys.argv[1:])
    myMachine=args.machine
    
    # Set the verbosity in the logger (loguru quirks ...)
    logger.remove()
    logger.add(sys.stderr, level=args.verbosity)
    icosPrepInstallDir=path.dirname(__file__)   
    sCmd='python '+str(icosPrepInstallDir)+'/dataHunting/dataHunter.py '
    
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
        logger.error('--ymf is a required parameter. You need to provide a Lumia yaml configuration file. icosPrep ships with an example.')
    else:
        ymlFile = args.ymf
        sCmd=sCmd+' --ymf='+str(ymlFile)
    if (not path.isfile(ymlFile)):
        logger.error(f"Fatal error in icosPrep: User specified configuration file {ymlFile} does not exist. Abort.")
        sys.exit(-33)
    if not(args.start is None):
        sCmd=sCmd+' --start='+str(args.start)
    if not(args.end is None):
        sCmd=sCmd+' --end='+str(args.end)
        
    script_directory=Path(icosPrepInstallDir)
    packageRootDir=script_directory.parent  # where .git directory lives.....
    sCmd=sCmd+' --rootDir='+str(packageRootDir)
    
    # Call the main data hunting method
    #ymlFile=prepareCallToLumiaGUI(ymlFile,  USE_TKINTER,  packageRootDir,  args)
    try:
        logger.info(sCmd)
        # system(sCmd)
    except:
        sys.exit('Abort. Call to dataHunter.py failed') 
    
    #from utils.housekeeping import caclulateSha256Filehash
    #sv=caclulateSha256Filehash('/home/arndt/data/backgroundCo2Concentrations/background_2019.nc')
    #print(f'sha256 value of background_2019.nc is: {sv}')
            
    from dataPrep.prepData import prepData
    # The ymlFile has been updated or execution has been aborted before getting to this point in the script....
    prepData(ymlFile, myMachine)
    
if __name__ == "__main__":
    main()

