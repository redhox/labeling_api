from pymongo import MongoClient
from pymongo.collection import Collection
import os
from dotenv import load_dotenv
load_dotenv()


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")

class MongoAccess:
    print("ici")
    def __init__(self):
        user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        pw = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        db_name = os.getenv("MONGO_DB")
        host =os.getenv("MONGO_HOST")
        self.client = MongoClient(f"mongodb+srv://{user}:{pw}@{host}")
        self.db = self.client[db_name]


    @property
    def users_collection(self) -> Collection:
        return self.db["image_table"]

    def initialize_db(self):
        print('inisialise  bbdd')
        required_collections = ['image_table'] 
        existing_collections = self.db.list_collection_names()

        for collection_name in required_collections:
            if collection_name not in existing_collections:
                self.db.create_collection(collection_name)
                print(f"Collection '{collection_name}' créée.")
            else:
                print(f"Collection '{collection_name}' existe déjà.")

    def incert_image(self,data):
        return self.db.images.insert_one(data)
        
    def change_label(self,image_id,data):
        return self.db.images.update_one(
            {"_id": image_id},  # Critère de sélection du document
            {"$set": {"label": data}}  # Opération de mise à jour
        )

    def phind_user(self,data):
        return self.db.images.find({'user': data})

    def phind_dir(self,data):
        return self.db.images.find({'dir': data})

    def phind_id(self,image_id):
        return self.db.images.find_one({'_id': image_id})