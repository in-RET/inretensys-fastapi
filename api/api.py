import os
import uuid

import docker

from InRetEnsys import *

from api import app, templates
from api.helpers import CreateComponentsList

from fastapi import Request, Response, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import List

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
IMAGE_TAG = "inretensys:0.2-gurobi"
CONTAINER_NAME = "inret-ensys-testcontainer"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get("/components/")
async def get_components_list():
    return JSONResponse(content={"components" : CreateComponentsList()})


@app.get("/components/{selectedType}")
async def get_component_schema(selectedType):
    if selectedType == "InRetEnsysModel":
        schemaData = InRetEnsysModel.schema_json()
    elif selectedType == "InRetEnsysBus":
        schemaData = InRetEnsysBus.schema_json()
    elif selectedType == "InRetEnsysFlow":
        schemaData = InRetEnsysFlow.schema_json()
    elif selectedType == "InRetEnsysSink":
        schemaData = InRetEnsysSink.schema_json()
    elif selectedType == "InRetEnsysSource":
        schemaData = InRetEnsysSource.schema_json()
    elif selectedType == "InRetEnsysNonConvex":
        schemaData = InRetEnsysNonConvex.schema_json()
    elif selectedType == "InRetEnsysInvestment":
        schemaData = InRetEnsysInvestment.schema_json()
    elif selectedType == "InRetEnsysTransformer":
        schemaData = InRetEnsysTransformer.schema_json()
    elif selectedType == "InRetEnsysEnergysystem":
        schemaData = InRetEnsysEnergysystem.schema_json()
    elif selectedType == "InRetEnsysStorage":
        schemaData = InRetEnsysStorage.schema_json()
    elif selectedType == "InRetEnsysConstraints":
        schemaData = InRetEnsysConstraints.schema_json()
    else:
        schemaData = None
        
    if schemaData is not None:
        return JSONResponse(content=schemaData)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/uploadFileBinary")
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...)):
    filelist = []
    
    for datafile in datafiles:
        filelist.append(await datafile.read())

    return run_simulation(request, input=filelist, ftype="bin")


@app.post("/uploadFileJson")
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...)):
    filelist = []
    
    for datafile in datafiles:
        filelist.append(await datafile.read())

    return run_simulation(request, input=filelist, ftype="json")


def generate_random_folder():
    return str(uuid.uuid4().hex)

@app.post("/runSimulation")
def run_simulation(request: Request, input=None, ftype=None, project="simulationen") -> Response:
    if input is not None:
        folderlist = []

        for file in input:
            workdir = os.path.join(os.getcwd(), project)
            foldername = generate_random_folder()
            outputdir = os.path.join(workdir, foldername)

            while os.path.exists(outputdir):
                foldername = generate_random_folder()
                outputdir = os.path.join(workdir, foldername)

            # Ordner anlegen
            os.makedirs(outputdir)
            
            # Festlegen der Parameter für den Start des Dockercontainers
            licensepath= os.path.join(os.getcwd(), 'gurobi_docker.lic')
            external_wdir = outputdir
            docker_wdir = "/app/working"

            if ftype == "json":
                savefile = open(os.path.join(outputdir, "config.json"), 'wb')
                configfile = os.path.join(docker_wdir, "config.json")
            else:
                savefile = open(os.path.join(outputdir, "config.bin"), 'wb')
                configfile = os.path.join(docker_wdir, "config.bin")
            savefile.write(file)
            savefile.close()

            # Verbindung zum Docker-Clienten herstellen (Server/Desktop Version)
            dock_client = docker.from_env()

            # Abfragen ob das Image existiert
            image = dock_client.images.list(IMAGE_TAG)

            # Wenn lokal kein Image existiert, wird dieses erstellt.
            if image == []:
                raise HTTPException(status_code=404, detail="Docker image not found")

            print("License: " + licensepath)
            print("Working: " + external_wdir)
            print("File: " + configfile)

            volumes_dict = {
                licensepath: {'bind': '/opt/gurobi/gurobi.lic', 'mode': 'ro'},
                external_wdir: {'bind': '/app/working', 'mode': 'rw'}
            }

            environmental_dict = {
                'FILE': configfile,
                'WDIR': docker_wdir
            }
            
            # Starten des docker-containers, im detach Mode, damit dieser das Python-Programm nicht blockiert
            container = dock_client.containers.run(
                IMAGE_TAG, 
                detach=True,
                volumes=volumes_dict,
                environment=environmental_dict,
                name=foldername
            )

            folderlist.append(foldername)

        return templates.TemplateResponse("submitted.html", {"request": request, "container_list": folderlist})
    else:
        raise HTTPException(status_code=404, detail="Input not given!")
