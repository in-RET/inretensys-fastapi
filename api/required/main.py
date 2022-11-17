import logging
import os
import sys
from pathlib import Path

from InRetEnsys import ModelBuilder
from InRetEnsys.common.log import InRetEnsysLogger

args = sys.argv[1:]

if len(args) > 0:
    configfile = args[0]
    workdir = args[1]
else:
    configfile = os.getenv('FILE', None)
    workdir = os.getenv('WDIR', None)

if configfile is not None and workdir is not None:
    dumpdir = os.path.join(workdir, "dumps")
    logdir = os.path.join(workdir, "logs")

    tmpfilename: str = os.path.basename(configfile)

    if tmpfilename.find(".json") > 0:
        dumpfile = os.path.join(dumpdir, tmpfilename.replace(".json", ".dump"))
        logfile = os.path.join(logdir, tmpfilename.replace(".json", ".log"))
    elif tmpfilename.find(".bin") > 0:
        dumpfile = os.path.join(dumpdir, tmpfilename.replace(".bin", ".dump"))
        logfile = os.path.join(logdir, tmpfilename.replace(".bin", ".log"))
    else:
        raise Exception("Fileformat is not valid!")

    if not os.path.exists(logfile):
        os.makedirs(os.path.dirname(logfile))   
        Path(logfile).touch()

    InRetEnsysLogger(name="logger", filename=logfile, level=logging.DEBUG)

    ModelBuilder(configfile, dumpfile, workdir, logdir, dumpdir)
else:
    raise Exception("Configuration and/or Workingdirectory not given!")
