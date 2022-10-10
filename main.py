import uvicorn
from InRetEnsysAPI import app

if __name__ == "__main__":
    uvicorn.run(app, app_dir="/InRetEnsysAPI", log_level="debug")