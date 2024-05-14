from bson import ObjectId
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional
import re


# Modèle de base pour l'utilisateur
class UserBase(BaseModel):
    """
    Classe de base pour les modèles d'utilisateur. Contient les champs communs à tous les modèles d'utilisateur.
    """
    username: str
    email: str

    @validator('email')
    def validate_email(cls, value):
        """
        Valide que l'adresse email est dans un format correct.

        Args:
            value (str): L'adresse email à valider.

        Raises:
            ValueError: Si l'adresse email n'est pas valide.

        Returns:
            str: L'adresse email validée.
        """
        
        return value



# Modèle de base pour l'utilisateur
class Usermail(BaseModel):
    """
    Classe de base pour les modèles demail.
    """
    email: str

    @validator('email')
    def validate_email(cls, value):
        """
        Valide que l'adresse email est dans un format correct.

        Args:
            value (str): L'adresse email à valider.

        Raises:
            ValueError: Si l'adresse email n'est pas valide.

        Returns:
            str: L'adresse email validée.
        """
        return value
# Modèle pour la création d'un utilisateur, inclut le mot de passe
class UserCreate(UserBase):
    """
    Modèle pour la création d'un utilisateur. Inclut un champ pour le mot de passe.
    """

    password: str

    @validator('password')
    def validate_password(cls, value):
        """
        Valide que le mot de passe a une longueur minimale.

        Args:
            value (str): Le mot de passe à valider.

        Raises:
            ValueError: Si le mot de passe est trop court.

        Returns:
            str: Le mot de passe validé.
        """
        if len(value) < 3:
            raise ValueError("Le mot de passe doit comporter au moins 3 caractères")
        return value

class UserLogin(BaseModel):
    """
    Modèle pour la création d'un utilisateur. Inclut un champ pour le mot de passe.
    """
    email: str
    password: str

class Userid(BaseModel):
    user_id: int



















# Modèle pour l'affichage d'un utilisateur, inclut l'ID
class UserDisplay(UserBase):
    """
    Modèle pour l'affichage des informations d'un utilisateur. Inclut l'ID de l'utilisateur.
    """
    id: str = Field(default="", alias="_id")

    # Utiliser un validateur pour convertir l'ObjectId en str si nécessaire
    @validator('id', pre=True, allow_reuse=True)
    def validate_id(cls, value):
        """
        Convertit un ObjectId MongoDB en string pour l'affichage.

        Args:
            value (ObjectId | str): L'ID de l'utilisateur à valider.

        Returns:
            str: L'ID de l'utilisateur sous forme de chaîne de caractères.
        """
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "id": "507f1f77bcf86cd799439011"  # Exemple d'ID MongoDB
            }
        }


# Modèle pour les opérations de mise à jour
class UserUpdate(BaseModel):
    """
    Modèle pour la mise à jour des informations d'un utilisateur. Permet de modifier le nom d'utilisateur, l'email et l'état actif.
    """
    username: Optional[str] = None
    email: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
