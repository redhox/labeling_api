# import psycopg2
# from psycopg2 import extras
# import os
from flask import Flask, jsonify, request
import psycopg2
import json
import bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
class PostgresAccess:
    def __init__(self):
        # Replace with your connection details
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
        )
        self.cursor = self.conn.cursor()

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of dictionaries containing user data.
        """
        self.cursor.execute("SELECT id, username, email FROM utilisateur;")
        users = self.cursor.fetchall()
        return users



    def create_user(self, username, email, password):
        """
        Creates a new user in the database.

        Args:
            data (dict): A dictionary containing user data.

        Returns:
            dict: A dictionary containing the created user data or an error message.
        """
        try:
            # Assuming data is a dictionary containing user input
            # username = data.get("username").replace("'", "\\'")
            # email = data.get("email").replace("'", "\\'")
            # password = data.get("password").replace("'", "\\'")

            password = self.hash_password(password)
            self.cursor.execute(
                """
                INSERT INTO utilisateur (username, email, password)
                VALUES (%s, %s, %s);
                """,
                (username, email, password),
            )
            self.conn.commit()
            return {"message": "Utilisateur créé avec succès."}
        except Exception as e:
            self.conn.rollback()
            return {"error": f"Erreur lors de la création de l'utilisateur: {str(e)}"}



    def get_user_by_id(self, user):
        """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: A dictionary containing the user data or an error message.
        """
        try:
            user_id=user.user_id
            print(f"SELECT id , email, username  FROM utilisateur WHERE id = {user_id};")
            self.cursor.execute("SELECT id , email, username  FROM utilisateur WHERE id = %s;", (user_id,))
            user = self.cursor.fetchone()
            if user:
                return user
            else:
                return jsonify({"error": "Utilisateur introuvable."})
        except Exception as e:
            return jsonify({"error": f"Erreur lors de la récupération de l'utilisateur: {str(e)}"})



    def get_user_by_email(self, user_email):
        """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: A dictionary containing the user data or an error message.
        """
        try:
            print("mail",user_email)
            self.cursor.execute(f"SELECT id, username, email FROM utilisateur WHERE email = %s;", (user_email,))
            user = self.cursor.fetchone()
            print("listeuser", user[0],user[1],user[2])
            user = {'id': user[0], 'username':user[1] , 'email':user[2]}
            if user:
                print("mail2: ",user)
                return user
            else:
                print("mail3")
                return {"error": "Utilisateur introuvable."}
        except Exception as e:
            print("mail4")
            return {"error": f"Erreur lors de la récupération de l'utilisateur: {str(e)}"}


    def delete_user_by_id(self, user):
        """
        Delete a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: A dictionary containing the user data or an error message.
        """
        try:
            user_id=user.user_id
            self.cursor.execute("GRANT DELETE ON TABLE utilisateur TO jean;")
            user = self.cursor.fetchone()
            print(user)
            print(f"DELETE FROM utilisateur WHERE id = {user_id};")

            self.cursor.execute("DELETE FROM utilisateur WHERE id = %s;", (user_id,))
            
            if user:
                return {"error": "Utilisateur delete."}
            else:
                return {"error": "Utilisateur introuvable."}
        except Exception as e:
            return {"error": f"Erreur lors de la récupération de l'utilisateur: {str(e)}"}


    def authenticate_user(self,email: str, password: str):
        """
        Vérifie si un utilisateur existe avec le mail d'utilisateur et le mot de passe fournis.

        Args:
            email (str): Le mail d'utilisateur de l'utilisateur.
            password (str): Le mot de passe de l'utilisateur.

        Returns:
            dict: Les données de l'utilisateur si les identifiants sont valides.

        Raises:
            HTTPException: Si les identifiants ne sont pas valides.
        """

        self.cursor.execute(f"SELECT password FROM utilisateur WHERE email = %s;", (email,))
        user = self.cursor.fetchone()
        print('user = ',user)

        if user is None:
            return None
        
        if not bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return None  
        return PostgresAccess().get_user_by_email(email)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash un mot de passe en utilisant bcrypt.

        Args:
            password (str): Le mot de passe à hacher.

        Returns:
            str: Le mot de passe hashé.

        Note:
            Bcrypt génère automatiquement un sel et l'incorpore dans le hash résultant.
        """
        # Convertir le mot de passe en bytes, puis le hasher
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Convertir le hash en string pour le stockage en base de données
        return hashed.decode('utf-8')
    
#     def update_user(self, user_id, data):
#         """
#         Updates a user's information in the database.

#         Args:
#             user_id (int): The ID of the user to update.
#             data (dict): A dictionary containing user data to update.

#         Returns:


# # import psycopg2
# # #         user="postgres.bnkdnaifyklvujuzixaq"
# # #         password="dMT2wRSi6h5Z31K5" 
# # #         host="aws-0-eu-west-2.pooler.supabase.com"
# # #         port=5432 
# # #         db_name="postgres"
# # # Connexion à la base de données
# # import psycopg2
# # from flask import Flask, jsonify, request

# # # Connexion à la base de données
# # conn = psycopg2.connect(
# #     dbname="username_base_de_données",
# #     user="username_utilisateur",
# #     password="password",
# #     host="localhost"
# # )

# # class User_bdd:
# #     def __init__(self, id, username,, email, password):
# #         self.id = id
# #         self.username = username
# #         self =
# #         self.email = email
# #         self.password = password

# #     def creer(self):
# #         # Implémenter la logique d'insertion d'un nouvel utilisateur

# #     def lire_tous(self):
# #         # Implémenter la logique de lecture de tous les utilisateurs

# #     def lire_par_id(self, id_utilisateur):
# #         # Implémenter la logique de lecture d'un utilisateur par ID

# #     def mettre_a_jour(self, id_utilisateur):
# #         # Implémenter la logique de mise à jour d'un utilisateur

# #     def supprimer(self, id_utilisateur):
# #         # Implémenter la logique de suppression d'un utilisateur


# # conn = psycopg2.connect(
# #     dbname="postgres",
# #     user="postgres.bnkdnaifyklvujuzixaq",
# #     password="dMT2wRSi6h5Z31K5",
# #     host="aws-0-eu-west-2.pooler.supabase.com"
# # )

# # # Créer un curseur pour exécuter des requêtes
# # cursor = conn.cursor()

# # # Créer la table utilisateur (si elle n'existe pas déjà)
# # cursor.execute("""
# # CREATE TABLE IF NOT EXISTS utilisateur (
# #     id SERIAL PRIMARY KEY,
# #     username VARCHAR(255) NOT NULL,
# #     email VARCHAR(255) UNIQUE NOT NULL,
# #     password VARCHAR(255) NOT NULL
# # );
# # """)
 
# # # Insérer un nouvel utilisateur
# # username = "Dupont"
# # email = "jean.dupont@example.com"
# # password = "motdepasse"

# # cursor.execute("""
# # INSERT INTO utilisateur (username, email, password)
# # VALUES (%s, %s, %s);
# # """, (username,email, password))

# # conn.commit()

# # # Lire tous les utilisateurs
# # cursor.execute("SELECT * FROM utilisateur;")
# # resultats = cursor.fetchall()

# # for utilisateur in resultats:
# #     print(f"ID: {utilisateur[0]} | username: {utilisateur[1]} | Préusername: {utilisateur[2]} | Email: {utilisateur[3]}")

# # # Mettre à jour un utilisateur
# # id_utilisateur = 1
# # nouveau_username = "Martin"

# # cursor.execute("""
# # UPDATE utilisateur
# # SET username = %s
# # WHERE id = %s;
# # """, (nouveau_username, id_utilisateur))

# # conn.commit()

# # # Supprimer un utilisateur
# # id_utilisateur = 2

# # cursor.execute("DELETE FROM utilisateur WHERE id = %s;", (id_utilisateur,))

# # conn.commit()

# # # Fermer la connexion à la base de données
# # conn.close()



# # class PostgresAccess:
# #     # def __init__(self):
# #     #     # user = os.getenv("POSTGRES_USER")
# #     #     # pw = os.getenv("POSTGRES_PASSWORD")
# #     #     # db_name = os.getenv("POSTGRES_DB", "webapi")
# #     #     # host = os.getenv("POSTGRES_HOST", "localhost")  # Optional, defaults to localhost
# #     #     # port = os.getenv("POSTGRES_PORT", 5432)  # Optional, defaults to standard port
# #     #     user="postgres.bnkdnaifyklvujuzixaq"
# #     #     pw="dMT2wRSi6h5Z31K5" 
# #     #     host="aws-0-eu-west-2.pooler.supabase.com"
# #     #     port=5432 
# #     #     db_name="postgres"

# #     #     self.conn = psycopg2.connect(
# #     #         user=user, password=pw, database=db_name, host=host, port=port
# #     #     )
# #     #     self.cur = self.conn.cursor()
# #     def __init__(self):
# #         user="postgres.bnkdnaifyklvujuzixaq"
# #         password="dMT2wRSi6h5Z31K5" 
# #         host="aws-0-eu-west-2.pooler.supabase.com"
# #         port=5432 
# #         db_name="postgres"

# #         try:
# #             self.connection = psycopg2.connect(
# #                 dbname=db_name,
# #                 user=user,
# #                 password=password,
# #                 host=host,
# #                 port=port
# #             )
# #             self.connection.autocommit = True  # Enable autocommit for simplicity
# #         except Exception as e:
# #             print(f"Error connecting to database: {e}")
# #             self.connection = None

# #     def initialize_db(self):
# #         self.cursor.execute("""
# #             CREATE TABLE IF NOT EXISTS users_db (
# #                 id SERIAL PRIMARY KEY,
# #                 username VARCHAR(255) NOT NULL,
# #                 email VARCHAR(255) NOT NULL,
# #                 password VARCHAR(255) NOT NULL
# #             );
# #         """)
# #         self.conn.commit()
# #         print(f"Table 'users_db' created.")

# #     def __del__(self):
# #         if self.connection:
# #             self.connection.close()

# #     @property
# #     def users_collection(self):
# #         return self._get_table("users_db")

# #     @property
# #     def sessions_table(self):
# #         return self._get_table("sessions_db")

# #     @property
# #     def prompt_table(self):
# #         return self._get_table("prompt_db")

# #     @property
# #     def users_table(self):
# #         return self._get_table("users_db")

# #     @property
# #     def sessions_table(self):
# #         return self._get_table("sessions_db")

# #     @property
# #     def prompt_table(self):
# #         return self._get_table("prompt_db")

# #     def _get_table(self, table_name):
# #         if self.connection:
# #             try:
# #                 cursor = self.connection.cursor()
# #                 cursor.execute(f"SELECT * FROM {table_name}")  # Replace with specific query if needed
# #                 return cursor
# #             except Exception as e:
# #                 print(f"Error accessing table {table_name}: {e}")
# #                 return None
# #         else:
# #             return None
        
# #     def get_all_users(self):
# #         # ... (rest of the code)

# #         users = []
# #         cursor = self.connection.cursor()  # Access cursor from PostgresAccess
# #         cursor.execute("SELECT id, email FROM users_db;")
# #         # ... (process cursor data and build users list)

# #         return users





# #     def get_user_by_mail():
# #         print()
# #     def get_db(self):
# #         return self.conn
    

# #     def get_all_sessions(self):
# #         self.cur.execute("SELECT * FROM sessions_db")
# #         return self.cur.fetchall()

# #     def get_sessions(self, skip: int = 0, limit: int = 10):
# #         self.cur.execute(
# #             "SELECT * FROM sessions_db LIMIT %s OFFSET %s", (limit, skip)
# #         )
# #         return self.cur.fetchall()

# #     def get_session(self, session_id):
# #         self.cur.execute("SELECT * FROM sessions_db WHERE id = %s", (session_id,))
# #         return self.cur.fetchone()

# #     def del_session(self, session_id):
# #         self.cur.execute("DELETE FROM sessions_db WHERE id = %s", (session_id,))
# #         self.conn.commit()

# #     def add_session(self, session_data):
# #         # Adapt this to your specific data structure (use psycopg2.extras.execute_values for bulk inserts)
# #         columns = ",".join(session_data.keys())
# #         placeholders = ",".join(["%s"] * len(session_data))
# #         insert_stmt = f"INSERT INTO sessions_db ({columns}) VALUES ({placeholders})"
# #         self.cur.execute(insert_stmt, list(session_data.values()))
# #         self.conn.commit()
# #         return self.cur.lastrowid  # Assuming your table has an auto-incrementing ID

# #     # Methods for users
# #     def add_user(self, user_data):
# #         columns = ",".join(user_data.keys())
# #         placeholders = ",".join(["%s"] * len(user_data))
# #         insert_stmt = f"INSERT INTO users_db ({columns}) VALUES ({placeholders})"
# #         self.cur.execute(insert_stmt, list(user_data.values()))
# #         self.conn.commit()
# #         return self.cur.lastrowid  # Assuming your table has an auto-incrementing ID

# #     def get_user(self, user_id):
# #         self.cur.execute("SELECT * FROM users_db WHERE id = %s", (user_id,))
# #         return self.cur.fetchone()

# #     def update_user(self, user_id, user_data):
# #         set_clause = ",".join([f"{key} = %s" for key in user_data.keys()])
# #         update_stmt = f"UPDATE users_db SET {set_clause} WHERE id = %s"
# #         self.cur.execute(update_stmt, list(user_data.values()) + [user_id])
# #         self.conn.commit()
# #         return self.cur.rowcount  # Number of rows affected

# #     def delete_user(self, user_id):
# #         self.cur.execute("DELETE FROM users_db WHERE id = %s", (user_id,))
# #         self.conn.commit()
# #         return self.cur.rowcount  # Number
