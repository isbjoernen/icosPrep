#!/usr/bin/env python

import os
import sys
#from shutil import copy2
from pathlib import Path
from loguru import logger
try:
    from utils.ymlSmartLoader import smartLoadYmlFile
except:
    from ymlSmartLoader import smartLoadYmlFile
try:
    from  dataPrep.obsCPortalDb import obsdb
except:
    from obsCPortalDb import obsdb
try:
    import utils.housekeeping as hk
except:
    import housekeeping as hk



def prepData(ymlFile, myMachine= 'UNKNOWN', includeBackground=True):
    # Read the yaml configuration file
    ymlContents=hk.readMyYamlFile(ymlFile, tryBkpFile=False, createBkpFile=False )

    # read yml config file
    sOutputPrfx=ymlContents['run']['thisRun']['uniqueOutputPrefix'] 
    sTmpPrfx=ymlContents['run']['thisRun']['uniqueTmpPrefix'] 
    sOutPath=ymlContents['run']['paths']['output']
    cwd = os.getcwd()
    logger.info(f'Current working directory is {cwd}')
    logger.info(f'run.paths.output is {sOutPath}')
    if not(os.path.isdir(sOutPath)):
        try:
            Path(sOutPath).mkdir(parents=True, exist_ok=True)
        except:
            sys.exit(f'Abort. Failed to create user-requested output directory {sOutPath}. Please check the key run.paths.output in your {ymlFile} file as well as your write permissions.')
    sTmpPath=ymlContents['run']['paths']['temp']
    logger.info(f'run.paths.rmp is {sTmpPath}')
    if not(os.path.isdir(sTmpPath)):
        try:
            Path(sTmpPath).mkdir(parents=True, exist_ok=True)
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
    


