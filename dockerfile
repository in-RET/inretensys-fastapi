FROM python:3.10

ENV NONROOT_USER=developer

ENV APP_ROOT /app
ENV INSTALL_ROOT /requirements
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd -g 1000 $NONROOT_USER && useradd -s /bin/bash -m -r -u 1000 -g $NONROOT_USER $NONROOT_USER
RUN echo "${NONROOT_USER}:${NONROOT_USER}" | chpasswd

#USER ${NONROOT_USER}

RUN mkdir ${APP_ROOT}
RUN mkdir ${INSTALL_ROOT}

COPY requirements/InRetEnsys-0.2a5-py3-none-any.whl ${INSTALL_ROOT}/InRetEnsys-0.2a5-py3-none-any.whl
COPY requirements/requirements.txt ${INSTALL_ROOT}/requirements.txt

RUN pip install --upgrade pip
RUN pip install ${INSTALL_ROOT}/InRetEnsys-0.2a5-py3-none-any.whl
RUN pip install -r ${INSTALL_ROOT}/requirements.txt

COPY api ${APP_ROOT}/api/

WORKDIR ${APP_ROOT}/

CMD ["python", "-m", "uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8001"]