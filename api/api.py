from InRetEnsys import *

from api import app
from api.helpers import CreateComponentsList

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return JSONResponse(content={"message" : "Schade Schokolade, dit geht... !"})


@app.get("/getComponentsList")
async def get_components_list():
    return JSONResponse(content={"components" : CreateComponentsList()})


@app.get("/getComponentSchema/{selectedType}")
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
        return HTTPException(404)

@app.post("/setComponentData/{selectedType}")
async def set_component_data(selectedType):
    return selectedType
