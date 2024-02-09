from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Vos fonctions personnalisées (assurez-vous qu'elles sont correctement définies)
from functions import read_first_column_of_csv, read_schedule

app = FastAPI()

# Configurez le chemin pour servir les fichiers statiques.
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# BASE_DIR doit pointer vers le répertoire qui contient le dossier 'frontend'.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

@app.get("/")
async def show_dropdown(request: Request):
    # Mettez à jour le chemin d'accès pour pointer vers le fichier csv correctement.
    file_path_schedule = os.path.join(BASE_DIR, "../dataset/NBASchedule23-24.csv")
    options = read_first_column_of_csv(file_path_schedule)
    return templates.TemplateResponse("firstpage.html", {"request": request, "options": options})

@app.get("/matches/{selected_date}")
async def get_matches_for_date(selected_date: str):
    # Même chose ici, assurez-vous que le chemin vers le fichier csv est correct.
    file_path_schedule = os.path.join(BASE_DIR, "../dataset/NBASchedule23-24.csv")
    schedule = read_schedule(file_path_schedule)
    matches = schedule.get(selected_date, [])
    return {"matches": matches}
