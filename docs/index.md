# inretensys-fastapi

## What is it?
inretensys-fastapi is an api which is based on FastAPI to connect a graphical user interface with the [inretensys-backend](https://github.com/in-RET/inretensys-backend).

This repository is part of the software package "inretensys-open-plan-gui" which is a fork of the [open_plan-gui](https://github.com/open-plan-tool/gui). 

## Differences to open_plan-gui
This package is the backend of the software package. It runs the interface to simulate und optimize generated energymodels from the graphical user interface.

It can run as a standalone interface or as part of an docker compose structure.

### standalone interface
To run inretensys-fastapi follow these steps.

* create a virtual environment for python (version > 3.8)
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
* install the requirements
```bash
$ pip install -r requirements.txt
```
For the following steps you need an energysystem as binary or json file.
How you generate these files please see [inretensys-backend](https://github.com/in-RET/inretensys-backend).

* run the cli with the following command to get an overview
```python
$ uvicorn api.api:app --reload #for debugging
```
After this step the webinterface is started and you can use the displayed link in your command line window.

### docker compose



## Use

To be done!