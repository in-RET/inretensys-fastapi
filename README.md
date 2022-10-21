# API for inretensys-backend

## Vorraussetzungen
- Python
- Docker
---
## Installation
Nach der Installation von Python (Version >3.6) und Docker sollte eine virtuelle Umgebung angelegt werden. Hierzu öffnen Sie bitte die Konsole/Terminal und navigieren in den Projektordner.

Eine virtuelle Pythonumgebung kann nun mit dem folgenden Befehl angelegt werden.

```
$ python -m venv .venv
```

Es wird ein weiterer Ordner erstellt mit dem namen ".venv". Unter Umständen kann dieser nicht sichtbar sein.

Aktivieren sie nun diese Umgebung mit
```
$ source venv/bin/activate
```

Nachfolgenden müssen alle benötigten Python-Packages installiert werden.

```
$ pip install -r api/requirements.txt
```

Nach Abschluss der installation kann das Projekt gestartet werden.

---
## Start der Software

### Uvicorn
````
$ uvicorn api.api:app --reload
````

Erreichbar ist die API + Dokumentation unter http://localhost:8000

### Gunicorn
````
$ gunicorn api.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
````

Erreichbar ist die API + Dokumentation unter http://localhost
