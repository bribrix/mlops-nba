# Utilisez une image de base officielle Python
FROM python:3.10-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY . /app

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port sur lequel uvicorn sera écouté
EXPOSE 8000

# Commande pour démarrer l'application via uvicorn
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--reload"]
