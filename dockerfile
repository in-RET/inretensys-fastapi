FROM python:3.10

ENV APP_ROOT /app
ENV INSTALL_ROOT /requirements

RUN mkdir ${APP_ROOT}
RUN mkdir ${INSTALL_ROOT}

COPY requirements/InRetEnsys-0.2a5-py3-none-any.whl ${INSTALL_ROOT}/InRetEnsys-0.2a5-py3-none-any.whl
COPY requirements/requirements.txt ${INSTALL_ROOT}/requirements.txt

RUN pip install --upgrade pip
RUN pip install ${INSTALL_ROOT}/InRetEnsys-0.2a5-py3-none-any.whl
RUN pip install -r ${INSTALL_ROOT}/requirements.txt

COPY api ${APP_ROOT}/api/

WORKDIR ${APP_ROOT}/
