# API for InRetEnsys

## Start with Uvicorn
uvicorn api.api:app --reload --bind 0.0.0.0:80

---

## Start with Gunicorn
gunicorn api.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

---

Erreichbar ist die Website folglich unter http://localhost
