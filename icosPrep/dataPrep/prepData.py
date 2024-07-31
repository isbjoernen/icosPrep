#!/usr/bin/env python

import os
import sys
from shutil import copy2
import datetime
from pandas import date_range
from numpy import  ndarray,  unique # , linspace
import yaml
from loguru import logger

#from dataclasses import dataclass, field
try:
    from utils.gridutils import Grid #, grid_from_rc
    from utils.ymlSmartLoader import smartLoadYmlFile
except:
    from gridutils import Grid #, grid_from_rc
    from ymlSmartLoader import smartLoadYmlFile

try:
    import dataPrep.readLv3NcFileFromCarbonPortal as fromICP # !
except:
    import readLv3NcFileFromCarbonPortal as fromICP
try:
    from  dataPrep.obsCPortalDb import obsdb
except:
    from obsCPortalDb import obsdb
try:
    import utils.housekeeping as hk
except:
    import housekeeping as hk
try:    
    from dataPrep import cdoWrapper
except:
    import cdoWrapper



def  readMyYamlFile(ymlFile, tryBkpFile=True):
    '''
    Function readMyYamlFile

    @param ymlFile : the LUMIA YAML configuration file in yaml (or rc) data format (formatted text)
    @type string (file name)
    @return contents of the ymlFile
    @type yamlObject
    '''
    ymlContents=None
    try:
        ymlContents=smartLoadYmlFile(ymlFile)
        if(ymlContents is None):
            tryBkpFile=True
    except:
        tryBkpFile=True
    if(tryBkpFile):
        #sCmd="cp "+ymlFile+'.bac '+ymlFile # recover from most recent backup file.
        #os.system(sCmd)
        src=str(ymlFile)+'.bac'
        try:
            copy2(src, ymlFile)
        except:
            pass
        try:
            ymlContents=smartLoadYmlFile(ymlFile)
        except:
            ymlContents=None
    if(ymlContents is None):
        logger.error(f"Abort! Unable to read the yaml configuration file {ymlFile} provided to icosPrep via the --ymf commandline option.")
        sys.exit(1)
    return(ymlContents)



def prepData(ymlFile, myMachine= 'UNKNOWN', includeBackground=True):
    # Read the yaml configuration file
    ymlContents=readMyYamlFile(ymlFile, False)

    # read yml config file
    sOutputPrfx=ymlContents['run']['thisRun']['uniqueOutputPrefix'] 
    sTmpPrfx=ymlContents['run']['thisRun']['uniqueTmpPrefix'] 
    sOutPath=ymlContents['run']['paths']['output']
    cwd = os.getcwd()
    logger.info(f'Current working directory is {cwd}')
    logger.info(f'run.paths.output is {sOutPath}')
    if not(os.path.isdir(sOutPath)):
        try:
            os.makedirs(sOutPath)
        except:
            sCmd=("mkdir -p "+str(sOutPath))
            try:
                os.system(sCmd)
            except:
                sys.exit(f'Abort. Failed to create user-requested output directory {sOutPath}. Please check the key run.paths.output in your {ymlFile} file as well as your write permissions.')
    sTmpPath=ymlContents['run']['paths']['temp']
    logger.info(f'run.paths.rmp is {sTmpPath}')
    if not(os.path.isdir(sTmpPath)):
        try:
            os.makedirs(sTmpPath)
        except:
            sCmd=("mkdir -p "+str(sTmpPath))
            try:
                os.system(sCmd)
            except:
                sys.exit(f'Abort. Failed to create user-requested output directory {sTmpPath}. Please check the key run.paths.temp in your {ymlFile} file as well as your write permissions.')

    # get tracer
    tracer=hk.getTracer(ymlContents['run']['tracers'])
    #defaults[f'emissions.{tracer}.archive'] = f'rclone:lumia:fluxes/nc/${{emissions.{tracer}.region}}/${{emissions.{tracer}.interval}}/'
    #start=ymlContents['run']['time']['start']
    #end=ymlContents['run']['time']['end']
    (start, bUseMachine)=hk.getStartEnd(ymlContents, 'start')
    (end,  bUseMachine)=hk.getStartEnd(ymlContents, 'end')

    # Load observations
    sLocation=ymlContents['observations'][tracer]['file']['location']
    # Create a proper output filename for all the combined observations. Need tracer and output directory etc.
    sOut=sTmpPrfx+"_dbg_AllObsData-withBg-"+tracer+".csv"
    if ('CARBONPORTAL' in sLocation):
        db = obsdb.from_CPortal(ymlContents=ymlContents, ymlFile=ymlFile)
        db.observations.to_csv( sOut, encoding='utf-8', mode='w', sep=',')
    #else:  NOTHING to do - it is already a local file
    #    from lumia.obsdb.InversionDb import obsdb
    #    db = obsdb.from_rc(rcf)
    #    db.observations.to_csv( sOut[:-4]+'-local.csv', encoding='utf-8', mode='w', sep=',')

    # Load the pre-processed emissions like fossil/EDGAR, marine, vegetation, ...:
    # sKeyword='LPJGUESS'
    logger.debug(f'Calling xrReader.Data.from_rc(rcf, start, end): start={start},  end={end}')
    import dataPrep.xrReader as xrReader
    emis = xrReader.Data.from_rc(ymlFile,  ymlContents, start, end, myMachine)
    logger.info('emis data read.')
    emis.print_summary()
    fName=sOutputPrfx+'emissions-apriori.nc'
    xrReader.WriteStruct(data=emis, fName=fName, zlib=False, complevel=1, only_transported=False)
    logger.info(f'Apriori emissions written to file {fName}.')
    


