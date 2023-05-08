import json
import os
import pickle
from InRetEnsys import InRetEnsysModel
from InRetEnsys.types import Solver

import docker
from fastapi.exceptions import HTTPException

from .constants import *

# IMAGE_TAG = "inretensys:0.2a4-gurobi"
CONTAINER_NAME = "inret-ensys-testcontainer"


def simulate_docker(configfile, foldername, ftype, file):
    root_work_dir = "/app/working"
    specific_work_dir = os.path.join(root_work_dir, foldername)
    external_work_dir = os.path.join(LOCAL_STORAGE_DIR, foldername)
    os.makedirs(specific_work_dir)

    licensepath = LICENSE_PATH

    if ftype == FTYPE_JSON:
        # Decoding for Website?!
        savefile = open(os.path.join(specific_work_dir, configfile), "wt")
    elif ftype == FTYPE_BINARY:
        savefile = open(os.path.join(specific_work_dir, configfile), "wb")
    savefile.write(file)
    savefile.close()

    # reload the system to get the solvertype
    reload_file = os.path.join(specific_work_dir, configfile)
    if reload_file.find(".json") > 0:
        xf = open(reload_file, "rt")
        model_dict = json.load(xf)
        model = InRetEnsysModel(**model_dict)
        xf.close()
    elif reload_file.find(".bin") > 0:
        xf = open(reload_file, "rb")
        model = pickle.load(xf)
        xf.close()
    else:
        raise Exception("Fileformat is not valid!")

    if model.solver == Solver.gurobi:
        IMAGE_TAG = "inretensys:0.2a5-gurobi"
        volumes_dict = {
            licensepath: {"bind": "/opt/gurobi/gurobi.lic", "mode": "ro"},
            external_work_dir: {"bind": root_work_dir, "mode": "rw"},
        }
    elif model.solver == Solver.cbc:
        IMAGE_TAG = "inretensys:0.2a5-cbc"
        volumes_dict = {external_work_dir: {"bind": root_work_dir, "mode": "rw"}}
    else:
        raise Exception("Solver not implemented yet.")

    configfile = os.path.join(root_work_dir, configfile)

    # Verbindung zum Docker-Clienten herstellen (Server/Desktop Version)
    docker_client = docker.from_env()

    # Abfragen ob das Image existiert
    image = docker_client.images.list(IMAGE_TAG)

    # Wenn lokal kein Image existiert, wird dieses erstellt.
    if image == []:
        raise HTTPException(status_code=404, detail="Docker image not found")

    # Starten des docker-containers, im detach Mode, damit dieser das Python-Programm nicht blockiert
    container = docker_client.containers.run(
        IMAGE_TAG,
        entrypoint=["python", "main.py"],
        command="-wdir /app/working " + configfile,
        detach=True,
        volumes=volumes_dict,
        name=foldername,
    )
