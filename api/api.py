import os
import stat
from typing import List

import paramiko
from api import app, templates
from fastapi import File, Form, Request, Response, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from InRetEnsys import *

from .constants import FTP_SERVER, FTYPE_BINARY, FTYPE_JSON
from .helpers import generate_random_folder
from .simulate_docker import simulate_docker
from .simulate_unirz import simulate_unirz

import docker

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


@app.post("/uploadFile")
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...), docker: str = Form(...), username: str = Form(default=None), password: str = Form(default=None)):
    filelist = []

    for datafile in datafiles:
        filelist.append((await datafile.read(), datafile.content_type))

    if docker == "docker":
        return run_simulation(request, input=filelist, container=True)
    else:
        return run_simulation(request, input=filelist, username=username, passwd=password)


@app.post("/uploadJson")
async def upload_file(request: Request, docker: bool, username: str="", password: str=""):
    return run_simulation(request, input=[(await request.json(), FTYPE_JSON)], external=True, container=docker, username=username, passwd=password)


def run_simulation(request: Request, input: list = None, external=False, container=False, username=None, passwd=None) -> Response:
    if input is not None:
        folderlist = []
        startscript = "#!/bin/csh\n"

        for datafile, ftype in input:
            workdir = os.path.join(os.getcwd(), "working")
            name_job = generate_random_folder()

            while os.path.exists(os.path.join(workdir, name_job)):
                name_job = generate_random_folder()

            if ftype == FTYPE_JSON:
                name_configfile = "config.json"
            elif ftype == FTYPE_BINARY:
                name_configfile = "config.bin"

            if container:
                simulate_docker(name_configfile, name_job, ftype, datafile)
            else:
                if username is None or passwd is None:
                    raise HTTPException(
                        status_code=401, detail="Authentification Error!")
                else:
                    simulate_unirz(name_configfile, name_job,
                                   ftype, datafile, str(username), str(passwd))
                    startscript += "cd " + name_job + "\n"
                    startscript += "bsub -q 'BatchXL' -J '" + name_job + "' batchscript.csh\n"
                    startscript += "cd ..\n"

                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.connect(FTP_SERVER, 22, username, passwd)

                with client.open_sftp() as sftp:
                    sftp.chdir("work")

                    with sftp.open("startskript.csh", "at") as sftp_file:
                        sftp_file.write(startscript)
                        sftp_file.close()
                    sftp.chmod("startskript.csh", stat.S_IRWXU)
                    sftp.close()

            folderlist.append(name_job)

        if not external:
            return templates.TemplateResponse("submitted.html", {"request": request, "container_list": folderlist})
        else:
            return JSONResponse(content={"folder": folderlist}, status_code=200, media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="Input not given!")


@app.post("/check/{foldername}")
async def check_container(foldername: str):
     # Verbindung zum Docker-Clienten herstellen (Server/Desktop Version)
    docker_client = docker.from_env()
    docker_container = docker_client.containers.get(foldername)
    
    return {"status": docker_container.status, "path": foldername} 


