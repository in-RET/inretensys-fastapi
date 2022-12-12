import os
import uuid
import paramiko
import stat
from typing import List

from api import app, templates
from fastapi import File, Request, Response, UploadFile, Form
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from InRetEnsys import *


from .constants import FTP_SERVER
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
async def upload_file(request: Request, datafiles: List[UploadFile] = File(...), docker: str = Form(...), username: str = Form(default=None), password: str = Form(default=None)):
    filelist = []

    for datafile in datafiles:
        filelist.append(await datafile.read())

    if docker == "docker":
        return run_simulation(request, input=filelist, ftype="fileJson", container=True)
    else:
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
        startscript = "#!/bin/csh\n"

        for datafile in input:
            workdir = os.path.join(os.getcwd(), parentfolder)
            name_job = generate_random_folder()

            while os.path.exists(os.path.join(workdir, name_job)):
                name_job = generate_random_folder()
                
            if ftype == "fileJson" or ftype == "Json":
                name_configfile = "config.json"
            elif ftype == "fileBin":
                name_configfile = "config.bin"
            
            if container:
                simulate_docker(parentfolder, name_configfile, name_job, ftype, datafile)
            else:
                if username is None or passwd is None:
                    raise HTTPException(status_code=401, detail="Authentification Error!")
                else:   
                    simulate_unirz(name_configfile, name_job, ftype, datafile, str(username), str(passwd))
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
        raise HTTPException(status_code=404, detail="Input not given!")
