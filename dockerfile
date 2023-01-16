FROM python:3.9-slim

WORKDIR /app

COPY InRetEnsys-0.2a4-py3-none-any.whl InRetEnsys-0.2a4-py3-none-any.whl
RUN pip install InRetEnsys-0.2a4-py3-none-any.whl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt