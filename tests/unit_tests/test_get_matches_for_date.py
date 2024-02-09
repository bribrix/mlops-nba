from fastapi.testclient import TestClient
from mlops_nba.backend import app

client = TestClient(app)

def test_get_matches_for_date():
    # Simuler une requête GET à l'endpoint avec une date sélectionnée
    response = client.get("/matches/2023-01-01")  # Utilisez une date qui correspond à votre jeu de données de test
    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
    assert isinstance(data["matches"], list)  # Assurez-vous que les matchs sont retournés sous forme de liste
