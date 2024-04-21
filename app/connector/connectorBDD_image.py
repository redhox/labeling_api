#connexion_API.py
from pymongo import MongoClient
from pymongo.collection import Collection
import os


class MongoAccess:
    def __init__(self):
        user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        pw = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        db_name = os.getenv("MONGO_DB", "webapi")
        self.client = MongoClient(f"mongodb://{user}:{pw}@mongodb:27017")
        self.db = self.client[db_name]

    @property
    def users_collection(self) -> Collection:
        return self.db["users_db"]
    
    @property
    def sessions_collection(self) -> Collection:
        return self.db["sessions_db"]

    @property
    def prompt_collection(self) -> Collection:
        return self.db["prompt_db"]

    # Cette méthode garantit que la BDD est toujours prête avec toutes les collections nécessaires avant que l'application commence à traiter les requêtes /
    def initialize_db(self):
        required_collections = ['users_db', 'sessions_db', 'prompt_db']  # Liste des noms de vos collections
        existing_collections = self.db.list_collection_names()

        for collection_name in required_collections:
            if collection_name not in existing_collections:
                self.db.create_collection(collection_name)
                print(f"Collection '{collection_name}' créée.")
            else:
                print(f"Collection '{collection_name}' existe déjà.")



    def get_db(self):
        return self.db

    def get_all_sessions(self):
        sessions = self.db.sessions.find({})
        return list(sessions)

    def get_sessions(self, skip: int = 0, limit: int = 10):
        sessions = self.db.sessions.find({}).skip(skip).limit(limit)
        return list(sessions)

    def get_session(self, session_id):
        session = self.db.sessions.find_one({"_id": session_id})
        return session

    def del_session(self, session_id):
        self.db.sessions.delete_one({'_id': session_id})

    def add_session(self, session_data):
        result = self.db.sessions.insert_one(session_data)
        return result.inserted_id

        # Méthodes pour les utilisateurs (certaines sont déjà définies dans votre fichier users.py)
    def add_user(self, user_data):
        result = self.users_collection.insert_one(user_data)
        return result.inserted_id

    def get_user(self, user_id):
        user = self.users_collection.find_one({"_id": user_id})
        return user

    def update_user(self, user_id, user_data):
        result = self.users_collection.update_one({"_id": user_id}, {"$set": user_data})
        return result.matched_count

    def delete_user(self, user_id):
        result = self.users_collection.delete_one({"_id": user_id})
        return result.deleted_count

    def get_prompt(self, prompt_id):
        prompt = self.prompt_collection.find_one({"prompt_id": prompt_id})
        return prompt

    def add_prompt(self, prompt_data:dict) -> str:
        result = self.prompt_collection.insert_one(prompt_data)
        return result.inserted_id

    def update_prompt(self, prompt_id, prompt_data):

        result = self.prompt_collection.update_one({"_id": prompt_id}, {"$set": prompt_data})
        return result.matched_count

    def delete_prompt(self, prompt_id) -> bool:
        result = self.prompt_collection.delete_one({"_id": prompt_id})
        return result.deleted_count > 0

    def get_all_prompts(self) -> list:
        prompts = self.prompt_collection.find({})
        return list(prompts)


















    # def __init__(self):
    #     self.client = MongoClient(f"mongodb://{self.__USER}:{self.__PW}@mongo:27017")
    #     self.db = self.client[self.__DB_NAME]
    #
    # def get_all_sessions(self):
    #     sessions = self.db.sessions.find({})
    #     return list(sessions)
    #
    # def get_sessions(self, skip: int = 0, limit: int = 10):
    #     sessions = self.db.sessions.find({}).skip(skip).limit(limit)
    #     return list(sessions)
    #
    # def get_session(self, id):
    #     session = self.db.sessions.find_one({"_id": id})
    #     return session
    #
    # def del_session(self, id):
    #     self.db.sessions.delete_one({'_id': id})
    #
    # def get_all_students(self):
    #     students = self.db.students.find({})
    #     return list(students)
    #
    # def get_students(self, skip: int = 0, limit: int = 10):
    #     students = self.db.students.find({}).skip(skip).limit(limit)
    #     return list(students)
    #
    # def get_student(self, id):
    #     student = self.db.students.find_one({"_id": id})
    #     return student
    #
    # def del_student(self, id):
    #     self.db.sessions.delete_one({'_id': id})
    #
    # def validate_session_data(self, session_data):
    #     required_fields = [
    #         "First_name",
    #         "Last_name",
    #         "Email",
    #         "Password",
    #         "Session_start",
    #         "Session_end",
    #         "ID"
    #     ]
    #     for field in required_fields:
    #         if field not in session_data or not session_data[field]:
    #             raise ValueError(f"Field '{field}' is required and cannot be empty.")
    #
    # def set_student(self, **session_data):
    #     self.validate_session_data(session_data)
    #     result = self.db.session.insert_one(session_data)
    #     inserted_id = result.inserted_id
    #     return self.get_session(str(inserted_id))
    #
    # def update_student(self, id, First_name, Last_name, Email, Password, Session_start, Session_end, ID ):
    #     student = {
    #         "First_name": First_name,
    #         "Last_name": Last_name,
    #         "Email": Email,
    #         "Password": Password,
    #         "Session_start": Session_start,
    #         "Session_end": Session_end,
    #         "ID": ID
    #     }
    #     self.db.session.update_one({"_id": id}, {'$set': student})
    #     return self.get_session(id)
    #
    #
    #     @property
    #     def users_collection(self):
    #         return self.db['users_db']