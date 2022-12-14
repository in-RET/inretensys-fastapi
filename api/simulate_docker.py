import os

import docker
from fastapi.exceptions import HTTPException

from .constants import *


def simulate_docker(parentfolder, configfile, foldername, ftype, file):
    # Lokalen Ordner anlegen
    outputdir = os.path.join(os.getcwd(), parentfolder, foldername)
    os.makedirs(outputdir)

    # Festlegen der Parameter für den Start des Dockercontainers
    licensepath = os.path.join(os.getcwd(), 'gurobi_docker.lic')
    docker_wdir = "/app/working"

    if ftype == FTYPE_JSON:
        savefile = open(os.path.join(outputdir, configfile), 'wt')
    elif ftype == FTYPE_BINARY:
        savefile = open(os.path.join(outputdir, configfile), 'wb')
    savefile.write(file)
    savefile.close()

    configfile = os.path.join(docker_wdir, configfile)

    # Verbindung zum Docker-Clienten herstellen (Server/Desktop Version)
    dock_client = docker.from_env()

    # Abfragen ob das Image existiert
    image = dock_client.images.list(IMAGE_TAG)

    # Wenn lokal kein Image existiert, wird dieses erstellt.
    if image == []:
        raise HTTPException(
            status_code=404, detail="Docker image not found")

    volumes_dict = {
        licensepath: {'bind': '/opt/gurobi/gurobi.lic', 'mode': 'ro'},
        outputdir: {'bind': docker_wdir, 'mode': 'rw'}
    }

    # Starten des docker-containers, im detach Mode, damit dieser das Python-Programm nicht blockiert
    container = dock_client.containers.run(
        IMAGE_TAG,
        #entrypoint=["/bin/bash" , "-c", "-it"],
        #command=["ls /app -axl"],
        entrypoint=["python", "main.py"],
        command="-wdir /app/working " + configfile,
        detach=True,
        volumes=volumes_dict,
        name=foldername,
    )