import logging.config
import yaml
import os

working_dir = os.getcwd()
print("working directory: ", working_dir)
conf = os.path.join(working_dir, "helpers/logging.conf")
logging.config.dictConfig(yaml.load(open(conf)))
logfile = logging.getLogger('file')
logconsole = logging.getLogger('console')


def log(str):
    # logfile.debug(str)
    logconsole.debug(str)
