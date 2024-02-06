from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Obtention du chemin absolu du répertoire courant où se trouve backend.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration de Jinja2 pour utiliser le chemin absolu des templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

@app.get("/")
async def read_root(request: Request):
    options = ["Option 1", "Option 2", "Option 3"]
    return templates.TemplateResponse("firstpage.html", {"request": request, "options": options})


