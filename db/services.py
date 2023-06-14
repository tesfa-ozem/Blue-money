# -*- coding: utf-8 -*-
from typing import List

from auth.schema import User
from core.security import hash_password
from core.utility import validate_email
from db.session import get_mongo_db
from pymongo.errors import PyMongoError


def add_user_service(email: str, password: str) -> User:
    try:
        # Validate the email format
        if not validate_email(email):
            raise ValueError("Invalid email format")
        # Hash password
        hashed_pwd = hash_password(password)
        db = get_mongo_db()
        collection = db["users"]
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


def update_user(user: User) -> User:
    ...


def delete_user(uid: List[str]) -> List[str]:
    # Delete a user or list of user
    ...
