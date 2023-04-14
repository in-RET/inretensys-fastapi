import os

FTP_SERVER = "csdata.tu-ilmenau.de"

FTYPE_BINARY = "application/octet-stream"
FTYPE_JSON = "application/json"

LOCAL_STORAGE_DIR = os.getenv("LOCAL_STORAGE_DIR", "/home/pyrokar/scratch5")
LICENSE_PATH = os.getenv(
    "GUROBI_LICENSE_FILE_PATH", os.path.join("/home/pyrokar/", "gurobi_docker.lic")
)
