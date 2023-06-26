# -*- coding: utf-8 -*-
from typing import List

from auth.schema import User

# importing ObjectId from bson library
from bson.objectid import ObjectId
from core.utility import validate_email
from db.session import get_mongo_db
from pymongo.errors import PyMongoError


def add_user_service(email: str, password: str) -> User:
    from core.security import hash_password

    try:
        # Validate the email format
        if not validate_email(email):
            raise ValueError("Invalid email format")
        # Hash password
        hashed_pwd = hash_password(password)
        db = get_mongo_db()
        collection = db["users"]
        collection.create_index([("email", 1)], unique=True)
        # Check if the email already exists in the collection
        existing_user = collection.find_one({"email": email})
        if existing_user:
            raise ValueError("Email already exists")

        user_data = {"email": email, "password": hashed_pwd}
        inserted_user = collection.insert_one(user_data)
        inserted_user_id = str(inserted_user.inserted_id)

        user = User(id=inserted_user_id, email=email)
        return user
    except PyMongoError as error:
        # Handle PyMongoError (MongoDB related errors)
        # Log the error or perform any other error handling actions
        # You can also raise a custom exception or return an error response
        print(f"An error occurred while adding a user: {error}")
        raise Exception("User registration failed.") from error
    except Exception as error:
        # Handle any other exceptions that might occur
        # Log the error or perform any other error handling actions
        print(f"An unexpected error occurred while adding a user: {error}")
        raise Exception(f"An unexpected error occurred, {error}")


def get_user(email: str):
    try:
        db = get_mongo_db()
        collection = db["users"]
        if not email:
            raise Exception("No email has been provided")
        user = collection.find_one({"email": email})
        if not user:
            return None  # User not found
        # user_object = User(id=user_id, email=user.get(email))
        return user

    except PyMongoError as error:
        # Handle PyMongoError (MongoDB related errors)
        # Log the error or perform any other error handling actions
        # You can also raise a custom exception or return an error response
        print(f"An error occurred while adding a user: {error}")
        raise Exception("User registration failed.") from error
    except Exception as error:
        # Handle any other exceptions that might occur
        # Log the error or perform any other error handling actions
        print(f"An unexpected error occurred while adding a user: {error}")
        raise Exception(f"An unexpected error occurred, {error}")


def get_user_by_id(user_id: str) -> User:
    try:
        objInstance = ObjectId(user_id)
        db = get_mongo_db()
        collection = db["users"]
        if not user_id:
            raise Exception("An unexpected error occurred")
        user = collection.find_one({"_id": objInstance})
        if not user:
            return None  # User not found
        #
        return User(id=user_id, email=user.get("email"))

    except PyMongoError as error:
        # Handle PyMongoError (MongoDB related errors)
        # Log the error or perform any other error handling actions
        # You can also raise a custom exception or return an error response
        print(f"An error occurred while adding a user: {error}")
        raise Exception("User registration failed.") from error
    except Exception as error:
        # Handle any other exceptions that might occur
        # Log the error or perform any other error handling actions
        print(f"An unexpected error occurred while adding a user: {error}")
        raise Exception(f"An unexpected error occurred, {error}")


def update_user(user: User):
    ...


def delete_user(uid: List[str]):
    # Delete a user or list of user
    ...
