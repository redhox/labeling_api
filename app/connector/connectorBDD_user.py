
from flask import Flask, jsonify, request
import psycopg2
import json
import bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
class PostgresAccess:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
        )
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilisateur (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(120) NOT NULL UNIQUE,
                password VARCHAR(128) NOT NULL,
                is_admin BOOLEAN DEFAULT false
            );
        """)
        self.conn.commit()



 



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
            self.cursor.execute(f"SELECT id, username, email, is_admin FROM utilisateur WHERE email = %s;", (user_email,))
            user = self.cursor.fetchone()
            print("listeuser", user[0],user[1],user[2],user[3])
            user = {'id': user[0], 'username':user[1] , 'email':user[2],'is_admin':user[3]}
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