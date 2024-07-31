
from loguru import logger
from os import getcwd
try:
    import yaml
except:
    print ('Fatal error:  Yaml library not available')
    quit()


def smartLoadYmlFile(ymlFile):
    try:
        with open(ymlFile, 'r') as file:
            ymlContents = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        myDir=getcwd()
        logger.info(f'smartLoadYmlFile finds itself in directory getcwd()={myDir}')
        logger.info(f'and cannot read the requested yaml file {ymlFile}. How unfortunate...')
        logger.info('If you are using the dataHunter web interface,  did you upload the yml file to the working directory on your server?')
        ymlContents=None
        logger.error(f"Error while parsing YAML file {ymlFile}")
        logger.error(f"Error reading YAML file: {exc}")
        return(None)
    return(ymlContents)





