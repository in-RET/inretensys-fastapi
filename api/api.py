import stat
import os
import uuid
from typing import List

import docker
from api import app, templates
from api.helpers import CreateComponentsList
from fastapi import File, Request, Response, UploadFile, Form
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from InRetEnsys import *
import paramiko

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

FTP_SERVER = "csdata.tu-ilmenau.de"
FTP_LOGIN = "alubojanski"
FTP_PWD = ""


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get("/components/")
async def get_components_list():
    return JSONResponse(content={"components": CreateComponentsList()})


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
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...), docker: str = Form(...)):
    filelist = []

    for datafile in datafiles:
        filelist.append(await datafile.read())

    if docker == "docker":
        return run_simulation(request, input=filelist, ftype="fileBin", container=True)
    elif docker == "ssh":
        return run_simulation(request, input=filelist, ftype="fileBin", container=False)
    else:
        return run_simulation(request, input=filelist, ftype="fileBin")


@app.post("/uploadFileJson")
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...), docker: str = Form(...)):
    filelist = []

    for datafile in datafiles:
        filelist.append(await datafile.read())

    if docker == "docker":
        return run_simulation(request, input=filelist, ftype="fileJson", container=True)
    elif docker == "ssh":
        return run_simulation(request, input=filelist, ftype="fileJson", container=False)
    else:
        return run_simulation(request, input=filelist, ftype="fileJson")


@app.post("/uploadJson")
async def upload_file(request: Request):
    # Only supports SSH actually
    return run_simulation(request, input=[await request.json()], ftype="Json", external=True)


def generate_random_folder():
    return str(uuid.uuid4().hex)


@app.post("/runSimulation")
def run_simulation(request: Request, input=None, ftype=None, parentfolder="work", external=False, container=False) -> Response:
    if input is not None:
        folderlist = []

        for file in input:
            workdir = os.path.join(os.getcwd(), parentfolder)
            foldername = generate_random_folder()
            outputdir = os.path.join(workdir, foldername)

            while os.path.exists(outputdir):
                foldername = generate_random_folder()
                outputdir = os.path.join(workdir, foldername)

            if ftype == "fileJson":
                configfile = "config.json"
            elif ftype == "fileBin":
                configfile = "config.bin"
            elif ftype == "Json":
                configfile = "config.json"

            if container:
                # Lokalen Ordner anlegen
                os.makedirs(outputdir)

                # Festlegen der Parameter für den Start des Dockercontainers
                licensepath = os.path.join(os.getcwd(), 'gurobi_docker.lic')
                external_wdir = outputdir
                docker_wdir = "/app/working"

                if ftype == "fileJson":
                    savefile = open(os.path.join(outputdir, configfile), 'wb')
                elif ftype == "fileBin":
                    savefile = open(os.path.join(outputdir, configfile), 'wb')
                elif ftype == "Json":
                    savefile = open(os.path.join(outputdir, configfile), 'wt')
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
            else:
                csh_value = {
                    'jobname': os.path.basename(outputdir),
                    'foldername': outputdir,
                    'configuration': os.path.basename(configfile)
                }

                csh_template = \
"""#!/bin/csh
#BSUB -q BatchXL
#BSUB -J "simulation_{jobname}"
#BSUB -L /bin/csh
#BSUB -eo logs/%J.err
#BSUB -oo logs/%J.log
#BSUB -n 48
#BSUB -cwd $HOME/work/{jobname}

pwd
module purge

source /usr/app-soft/anaconda3/etc/profile.d/conda.csh

module load python/anaconda3

conda env list
conda env create --file environment.yaml
conda activate simulation_environment

which python

pip install InRetEnsys-0.2a2-py3-none-any.whl

module load gurobi/v911
echo $GRB_LICENSE_FILE

setenv GUROBI_HOME /usr/app-soft/gurobi/gurobi911/linux64/
setenv PATH ${{PATH}}:${{GUROBI_HOME}}/bin 
setenv LD_LIBRARY_PATH ${{LD_LIBRARY_PATH}}:${{GUROBI_HOME}}/lib

setenv FILE {configuration}
setenv WDIR ${{PWD}}

python main.py
""".format(**csh_value)

                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.connect(FTP_SERVER, 22, FTP_LOGIN, FTP_PWD)
                
                with client.open_sftp() as sftp:
                    sftp.chdir("work")
                    sftp.mkdir(csh_value['jobname'])
                    sftp.chdir(csh_value['jobname'])
                    with sftp.open("batchscript.csh", "wt") as sftp_file:
                        sftp_file.write(csh_template)
                        sftp_file.close()
                    sftp.chmod("batchscript.csh", stat.S_IRWXU)

                    if ftype == "fileJson":
                        sftp_file = sftp.open("config.json", 'wb')
                    elif ftype == "fileBin":
                        sftp_file = sftp.open("config.bin", 'wb')
                    elif ftype == "Json":
                        sftp_file = sftp.open("config.json", 'wt')
                    sftp_file.write(file)
                    sftp_file.close()       
                    

                    print(os.getcwd())
                    sftp.put(os.path.join(os.getcwd(), "api", "required", "environment.yaml"), "environment.yaml") 
                    sftp.put(os.path.join(os.getcwd(), "api", "required", "InRetEnsys-0.2a2-py3-none-any.whl"), "InRetEnsys-0.2a2-py3-none-any.whl")
                    sftp.put(os.path.join(os.getcwd(), "api", "required", "main.py"), "main.py")

                    sftp.close()
    
        if not external:
            return templates.TemplateResponse("submitted.html", {"request": request, "container_list": folderlist})
    else:
        raise HTTPException(status_code=404, detail="Input not given!")
