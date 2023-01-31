import os

IMAGE_TAG = "inretensys:0.2a4-gurobi"
CONTAINER_NAME = "inret-ensys-testcontainer"

FTP_SERVER = "csdata.tu-ilmenau.de"

FTYPE_BINARY = "application/octet-stream"
FTYPE_JSON = "application/json"

LOCAL_STORAGE_DIR = os.getenv("LOCAL_STORAGE_DIR", "/home/pyrokar/scratch5")