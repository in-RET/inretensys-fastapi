import os
import stat
import docker
import paramiko

from typing import List
from fastapi import FastAPI, File, Form, Request, Response, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from InRetEnsys import *

from .helpers import generate_random_folder
from .docker import simulate_docker
from .constants import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="api/static"), name="static")

templates = Jinja2Templates(directory="api/templates")

origins = ["http://localhost", "http://localhost:8000"]

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


@app.post("/uploadFile")
async def upload_file(
    request: Request,
    datafiles: List[UploadFile] = File(...),
):
    filelist = []

    for datafile in datafiles:
        filelist.append((await datafile.read(), datafile.content_type))

    return run_simulation(request, input=filelist)


@app.post("/uploadJson")
async def upload_file(request: Request):

    return run_simulation(
        request,
        input=[(await request.json(), FTYPE_JSON)],
        external=True,
    )


def run_simulation(request: Request, input: list = None, external=False) -> Response:
    if input is None:
        raise HTTPException(
            status_code=404, detail="No Input given!"
        )
    else:
        folderlist = []
        workdir = os.path.join(os.getcwd(), "working")
        
        for datafile, ftype in input:
            nameOfJob = generate_random_folder()

            while os.path.exists(os.path.join(workdir, nameOfJob)):
                nameOfJob = generate_random_folder()

            if ftype == FTYPE_JSON:
                nameOfConfigFile = "config.json"
            elif ftype == FTYPE_BINARY:
                nameOfConfigFile = "config.bin"

            simulate_docker(nameOfConfigFile, nameOfJob, ftype, datafile)
            folderlist.append(nameOfJob)

        if not external:
            return templates.TemplateResponse(
                "submitted.html", {"request": request, "container_list": folderlist}
            )
        else:
            return JSONResponse(
                content={"folder": folderlist},
                status_code=200,
                media_type="application/json",
            )


@app.post("/check/{token}")
async def check_container(token: str):
    # Verbindung zum Docker-Clienten herstellen (Server/Desktop Version)
    docker_client = docker.from_env()
    docker_container = docker_client.containers.get(token)

    if docker_container.status == "exited":
        return_status = "DONE"
    else:
        return_status = "PENDING"

    return JSONResponse(
        content={"status": return_status, "token": token},
        status_code=200,
        media_type="application/json",
    )
