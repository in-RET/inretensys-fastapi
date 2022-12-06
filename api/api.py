import os
import uuid
from typing import List

from api import app, templates
from api.helpers import CreateComponentsList
from fastapi import File, Request, Response, UploadFile, Form
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from InRetEnsys import *

from .simulate_docker import simulate_docker
from .simulate_unirz import simulate_unirz

origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...), docker: str = Form(...), username: str = Form(...), password: str = Form(...)):
    filelist = []

    for datafile in datafiles:
        filelist.append(await datafile.read())

    if docker == "docker":
        return run_simulation(request, input=filelist, ftype="fileBin", container=True)
    else:
        return run_simulation(request, input=filelist, ftype="fileBin", username=username, passwd=password)


@app.post("/uploadFileJson")
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...), docker: str = Form(...), username: str = Form(...), password: str = Form(...)):
    filelist = []

    for datafile in datafiles:
        filelist.append(await datafile.read())

    if docker == "docker":
        return run_simulation(request, input=filelist, ftype="fileJson", container=True)
    else:
        print("Username:", username)
        print("Password:", password)
        return run_simulation(request, input=filelist, ftype="fileJson", username=username, passwd=password)
        

@app.post("/uploadJson")
async def upload_file(request: Request, username: str, password: str, docker: bool):
    return run_simulation(request, input=[await request.json()], ftype="Json", external=True, container=docker, username=username, passwd=password)


def generate_random_folder():
    return str(uuid.uuid4().hex)


@app.post("/runSimulation")
def run_simulation(request: Request, input=None, ftype=None, parentfolder="work", external=False, container=False, username=None, passwd=None) -> Response:
    if input is not None:
        folderlist = []

        for datafile in input:
            workdir = os.path.join(os.getcwd(), parentfolder)
            name_job = generate_random_folder()

            while os.path.exists(os.path.join(workdir, name_job)):
                name_job = generate_random_folder()
                
            if ftype == "fileJson":
                name_configfile = "config.json"
            elif ftype == "fileBin":
                name_configfile = "config.bin"
            elif ftype == "Json":
                name_configfile = "config.json"

            if container:
                simulate_docker(parentfolder, name_configfile, name_job, ftype, datafile)
            else:
                if username is None or passwd is None:
                    raise HTTPException(status_code=404, detail="Authentification failed!")
                else:   
                    simulate_unirz(name_configfile, name_job, ftype, datafile, username, passwd)

            folderlist.append(name_job)

        if not external:
            return templates.TemplateResponse("submitted.html", {"request": request, "container_list": folderlist})
    else:
        raise HTTPException(status_code=404, detail="Input not given!")
