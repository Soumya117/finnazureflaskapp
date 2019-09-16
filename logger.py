import logging, logging.config, yaml

logging.config.dictConfig(yaml.load(open('logging.conf')))
logfile    = logging.getLogger('file')
logconsole = logging.getLogger('console')

def log(str):
     logfile.debug(str)
     logconsole.debug(str)