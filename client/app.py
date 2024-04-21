import requests

# URL de la route protégée
# url = "http://localhost:8002/users/protected_route"
url = "http://localhost:8002/users/"

# Votre token d'authentification
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb2lAbWFpbC5jb20iLCJleHAiOjE3MTM1MzI1NjV9.R1rwPKNOIrICZDZXJSHhoikgL88a1MrTRGM1koukBLM"

# En-têtes de la requête
headers = {
    "Authorization": f"Bearer {token}"
}

# Envoyer la requête GET
# response = requests.get(url, headers=headers)
response = requests.get(url)

# Afficher la réponse
print(response.json())
