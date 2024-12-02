# Minio Bucket Manager

Ce module contient les classes pour gérer les opérations de base sur un bucket MinIO (comme l'upload et la liste des objets) et pour les artefacts spécifiques de MLflow.

## Classes

### MinioBucketManager
::: app.connector.connectorBucket.MinioBucketManager

- **`test_connection`** : Teste la connexion au bucket en listant les objets.
- **`upload_file`** : Télécharge un fichier local dans le bucket S3.
- **`list_objects`** : Liste tous les objets dans le bucket.

---

### MinioBucketMLflow

::: app.connector.connectorBucket.MinioBucketMLflow

- **`get_artifact`** : Récupère les artefacts, comme les images et les modèles, depuis le bucket MLflow.
- **`dl_model`** : Télécharge un modèle spécifique depuis le bucket MinIO et l'enregistre localement.
