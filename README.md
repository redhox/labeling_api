# FastAPI pour le projet Manag'IA

Une courte description de votre projet et ce qu'il fait.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les composants suivants :
- Python 3.8+
- pip

# **Installation**

Voici les étapes pour l'installation:

```bash
git clone https://your-repository-url.git
cd your-repository-name
pip install -r requirements.txt
```
# **Utilisation**

Démarrer le serveur FastAPI :

```bash
uvicorn main:app --reload
```
Cela lancera le serveur de développement et permettra le rechargement automatique pour faciliter le développement.


# **Routes**

Pour avoir un vision d'ensemble des routes disponibles, vous pouvez visiter la documentation interactive de l'API à l'adresse suivante : 
```
http://localhost:8002/docs
```
![FastapiSwagger](//api-filee/fastapi.jpg "Swagger UI") 


# **Déploiement** 

Instructions sur comment déployer l'API sur un serveur. Par exemple, avec Uvicorn :

```bash
uvicorn.run(app, host="0.0.0.0", port=8002)
```
# **Tests**

Expliquez comment lancer les tests pour votre système :

pour ce faire il suffit de lancer la commande suivante :

```
pytest
```


