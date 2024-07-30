
from loguru import logger
try:
    import yaml
except:
    print ('Fatal error:  Yaml library not available')
    quit()


def smartLoadYmlFile(ymlFile):
    try:
        with open(ymlFile, 'r') as file:
            ymlContents = yaml.safe_load(file)
            return(ymlContents)
    except yaml.YAMLError as exc:
        ymlContents=None
        logger.error(f"Error while parsing YAML file {ymlFile}")
        logger.error(f"Error reading YAML file: {exc}")
        return(None)





