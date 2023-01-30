import os

import docker
from fastapi.exceptions import HTTPException

from .constants import *


def simulate_docker(configfile, foldername, ftype, file):
    # Lokalen Ordner anlegen

    root_work_dir = "/app/working"
    specific_work_dir = os.path.join(root_work_dir, foldername)
    external_work_dir = os.path.join(os.getenv("LOCAL_STORAGE_DIR", "/home/pyrokar/scratch4"), foldername)
    os.makedirs(specific_work_dir)


    # Festlegen der Parameter für den Start des Dockercontainers
    licensepath = os.getenv("GUROBI_LICENSE_FILE_PATH", os.path.join("/home/pyrokar/", "gurobi_docker.lic"))

    if ftype == FTYPE_JSON:
        # Decoding for Website?!
        savefile = open(os.path.join(specific_work_dir, configfile), 'wt')
    elif ftype == FTYPE_BINARY:
        savefile = open(os.path.join(specific_work_dir, configfile), 'wb')
    savefile.write(file)
    savefile.close()

    configfile = os.path.join(root_work_dir, configfile)

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
        external_work_dir: {'bind': root_work_dir, 'mode': 'rw'}
    }

    # Starten des docker-containers, im detach Mode, damit dieser das Python-Programm nicht blockiert
    container = dock_client.containers.run(
        IMAGE_TAG,
        entrypoint=["python", "main.py"],
        command="-wdir /app/working " + configfile,
        detach=True,
        volumes=volumes_dict,
        name=foldername,
    )