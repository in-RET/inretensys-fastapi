import uvicorn
from api import app

if __name__ == "__main__":
    uvicorn.run(app, app_dir="/api", log_level="debug")