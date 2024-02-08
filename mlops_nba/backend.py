from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import csv
from functions import read_first_column_of_csv, read_schedule

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Obtention du chemin absolu du répertoire courant où se trouve backend.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration de Jinja2 pour utiliser le chemin absolu des templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))


@app.get("/")
async def show_dropdown(request: Request):
    file_path_schedule = f"../dataset/NBASchedule23-24.csv"
    options = read_first_column_of_csv(file_path_schedule)  # Ajustez le chemin d'accès au fichier CSV
    return templates.TemplateResponse("firstpage.html", {"request": request, "options": options})


# Nouvelle route pour récupérer les matchs basée sur une date
@app.get("/matches/{selected_date}")
async def get_matches_for_date(selected_date: str):
    file_path_schedule = os.path.join(BASE_DIR, "../dataset/NBASchedule23-24.csv")  # Ajustez le chemin
    schedule = read_schedule(file_path_schedule)
    matches = schedule.get(selected_date, [])
    return {"matches": matches}