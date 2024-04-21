# from pymongo.collection import Collection
# from bson import ObjectId
# from app.models.users_model import UserCreate, UserUpdate
# from app.connector.connectorBDD_user import PostgresAccess
# from fastapi import HTTPException
# import bcrypt


# class UserCRUD:
#     def __init__(self):
#         """
#         Initialise une nouvelle instance de la classe UserCRUD pour gérer les opérations CRUD sur les utilisateurs.

#         Args:
#             user_db (Collection): Une instance de Collection de pymongo pointant vers la base de données des utilisateurs.
#         """
    

#     # def create_user(self, user_data: UserCreate):
#     #     """
#     #     Crée un nouvel utilisateur dans la base de données après vérification de l'unicité de l'email.

#     #     Args:
#     #         user_data (UserCreate): Un objet contenant les données de l'utilisateur à créer.

#     #     Returns:
#     #         dict: Les données de l'utilisateur créé.

#     #     Raises:
#     #         HTTPException: Si un utilisateur avec le même email existe déjà.
#     #     """
#     #     if self.db.find_one({"email": user_data.email}):
#     #         raise HTTPException(status_code=400, detail="Email already registered")
#     #     user_data_dict = user_data.dict()
#     #     # Assume hashing password or other preparations here
#     #     user_data_dict["password"] = self.hash_password(user_data_dict["password"])
#     #     result = self.db.insert_one(user_data_dict)
#     #     new_user_id = result.inserted_id
#     #     return self.db.find_one({"_id": new_user_id})
#     def create_user(self, user_data: UserCreate):
#         """
#         Crée un nouvel utilisateur dans la base de données après vérification de l'unicité de l'email.

#         Args:
#             user_data (UserCreate): Un objet contenant les données de l'utilisateur à créer.

#         Returns:
#             dict: Les données de l'utilisateur créé.

#         Raises:
#             HTTPException: Si un utilisateur avec le même email existe déjà.
#         """
#         print("crud ?")
#         if self.check_user_exists(user_data.email):
#             raise HTTPException(status_code=400, detail="Email already registered")

#         user_data_dict = user_data.dict()
#         cursor = self.connection.cursor()

#         # Construct the INSERT query dynamically
#         insert_query = f"""
#             INSERT INTO users_db (email, password, username, is_active, created_at)
#             VALUES (%s, %s, %s, %s, %s)
#             RETURNING *;  -- Retrieve the inserted user data
#         """

#         cursor.execute(insert_query, (
#             user_data_dict["email"],
#             user_data_dict["password"],
#             user_data_dict["username"],
#         ))

#         inserted_user_row = cursor.fetchone()  # Get the inserted user row

#         if not inserted_user_row:
#             raise HTTPException(status_code=500, detail="Failed to create user")

#         return {key: value for key, value in zip(cursor.description, inserted_user_row)}


#     def get_user(self, user_id: str) -> dict:
#         """
#         Récupère un utilisateur par son ID.

#         Args:
#             user_id (str): L'ID de l'utilisateur à récupérer.

#         Returns:
#             dict: Les données de l'utilisateur si trouvé, sinon None.
#         """
#         return self.db.find_one({"_id": ObjectId(user_id)})

#     def get_all_users(self):
#         """
#         Récupère tous les utilisateurs de la base de données.

#         Returns:
#             list: Une liste contenant les données de tous les utilisateurs.
#         """
#         users = PostgresAccess.get_all_users(self)
#         return list(users)

#     def get_user_by_id(self, user_id: str):
#         """
#         Récupère un utilisateur par son ID, similaire à get_user mais avec gestion des erreurs.

#         Args:
#             user_id (str): L'ID de l'utilisateur à récupérer.

#         Returns:
#             dict: Les données de l'utilisateur si trouvé.

#         Raises:
#             HTTPException: Si aucun utilisateur avec cet ID n'est trouvé.
#         """
#         user = self.db.find_one({"_id": ObjectId(user_id)})
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user

#     def get_user_by_email(self, email: str):
#         """
#         Récupère un utilisateur par son email.

#         Args:
#             email (str): L'email de l'utilisateur à récupérer.

#         Returns:
#             dict: Les données de l'utilisateur si trouvé.

#         Raises:
#             HTTPException: Si aucun utilisateur avec cet email n'est trouvé.
#         """
#         user = self.db.find_one({"email": email})
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         #suprime le password
#         user = {key: value for key, value in user.items() if key != 'password'}
#         return user

#     def update_user(self, user_id: str, user: UserUpdate) -> dict:
#         """
#         Met à jour un utilisateur existant dans la base de données.

#         Args:
#             user_id (str): L'ID de l'utilisateur à mettre à jour.
#             user (UserUpdate): Un objet contenant les champs à mettre à jour.

#         Returns:
#             dict: Les données mises à jour de l'utilisateur.

#         Note:
#             Si un mot de passe est fourni, il est d'abord hashé avant la mise à jour.
#         """
#         update_data = user.dict(exclude_unset=True)
#         if "password" in update_data:
#             update_data["password"] = self.hash_password(update_data["password"])
#         self.db.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
#         return self.db.find_one({"_id": ObjectId(user_id)})

#     def delete_user(self, user_id: str) -> bool:
#         """
#         Supprime un utilisateur de la base de données en utilisant son ID.

#         Args:
#             user_id (str): L'ID de l'utilisateur à supprimer.

#         Returns:
#             bool: True si la suppression a été effectuée, sinon une exception est levée.

#         Raises:
#             HTTPException: Si aucun utilisateur avec cet ID n'est trouvé.
#         """
#         result = self.db.delete_one({"_id": ObjectId(user_id)})
#         if result.deleted_count == 0:
#             raise HTTPException(status_code=404, detail="User not found")
#         return True  # Retourne True si la suppression a été effectuée

#     def authenticate_user(self,email: str, password: str):
#         """
#         Vérifie si un utilisateur existe avec le mail d'utilisateur et le mot de passe fournis.

#         Args:
#             email (str): Le mail d'utilisateur de l'utilisateur.
#             password (str): Le mot de passe de l'utilisateur.

#         Returns:
#             dict: Les données de l'utilisateur si les identifiants sont valides.

#         Raises:
#             HTTPException: Si les identifiants ne sont pas valides.
#         """
#         user = self.db.find_one({"email": email})
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
#             raise HTTPException(status_code=400, detail="Incorrect password")
#         return user
    
#     @staticmethod
#     def hash_password(password: str) -> str:
#         """
#         Hash un mot de passe en utilisant bcrypt.

#         Args:
#             password (str): Le mot de passe à hacher.

#         Returns:
#             str: Le mot de passe hashé.

#         Note:
#             Bcrypt génère automatiquement un sel et l'incorpore dans le hash résultant.
#         """
#         # Convertir le mot de passe en bytes, puis le hasher
#         hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         # Convertir le hash en string pour le stockage en base de données
#         return hashed.decode('utf-8')

