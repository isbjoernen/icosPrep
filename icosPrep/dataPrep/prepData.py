#!/usr/bin/env python

import os
import sys
import datetime
from pandas import date_range
from numpy import  ndarray,  unique # , linspace
import yaml
from loguru import logger

#from dataclasses import dataclass, field
from utils.gridutils import Grid #, grid_from_rc

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



def  readMyYamlFile(ymlFile):
    '''
    Function readMyYamlFile

    @param ymlFile : the LUMIA YAML configuration file in yaml (or rc) data format (formatted text)
    @type string (file name)
    @return contents of the ymlFile
    @type yamlObject
    '''
    ymlContents=None
    try:
        with open(ymlFile, 'r') as file:
            ymlContents = yaml.safe_load(file)
    except:
        sCmd="cp "+ymlFile+'.bac '+ymlFile # recover from most recent backup file.
        os.system(sCmd)
        try:
            with open(ymlFile, 'r') as file:
                ymlContents = yaml.safe_load(file)
            #sCmd="cp "+ymlFile+' '+ymlFile+'.bac' # This is now already done in housekeeping.py, which is more consistent
            #os.system(sCmd)
        except:
            logger.error(f"Abort! Unable to read yaml configuration file {ymlFile} - failed to read its contents with yaml.safe_load()")
            sys.exit(1)
    return(ymlContents)



def prepData(ymlFile, myMachine= 'UNKNOWN'):
    # Read the yaml configuration file
    ymlContents=readMyYamlFile(ymlFile)
    # read yml config file
    sOutputPrfx=ymlContents['run']['thisRun']['uniqueOutputPrefix'] 
    sTmpPrfx=ymlContents['run']['thisRun']['uniqueTmpPrefix'] 
    sOutPath=ymlContents['run']['paths']['output']

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
    logger.debug(f'xr.Data.from_rc(rcf, start, end): start={start},  end={end}')
    emis = xr.Data.from_rc(rcf, start, end)
    logger.info('emis data read.')
    # TODO: the df is for debugging only - remove later
    try:
        df = emis.to_dataframe()
        df.iloc[:512, :].to_csv('_dbg_emDataA_emissions_aPriori-XrL872.csv', mode='w', sep=',')
        dStep=int(len(df)/3)
        df.iloc[dStep:dStep+512, :].to_csv('_dbg_emDataB_emissions_aPriori-XrL872.csv', mode='w', sep=',')
        dStep+=dStep
        df.iloc[dStep:dStep+512, :].to_csv('_dbg_emDataC_emissions_aPriori-XrL872.csv', mode='w', sep=',')
    except:
        pass
    emis.print_summary()


