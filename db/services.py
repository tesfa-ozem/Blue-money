# -*- coding: utf-8 -*-
from typing import List

from auth.schema import User

from bson.objectid import ObjectId
from core.utility import validate_email
from db.session import get_mongo_db
from graphql import GraphQLError


def add_user_service(email: str, password: str) -> User:
    from core.security import hash_password

    if not validate_email(email):
        raise GraphQLError(
            message="Invalid email format",
            extensions={
                "code": "BAD_REQUEST",
            },
        )
    # Hash password
    hashed_pwd = hash_password(password)
    db = get_mongo_db()
    collection = db["users"]
    collection.create_index([("email", 1)], unique=True)
    # Check if the email already exists in the collection
    existing_user = collection.find_one({"email": email})
    if existing_user:
        raise GraphQLError(
            message="Email already exists",
            extensions={
                "code": "BAD_REQUEST",
            },
        )

    user_data = {"email": email, "password": hashed_pwd}
    inserted_user = collection.insert_one(user_data)
    inserted_user_id = str(inserted_user.inserted_id)

    user = User(id=inserted_user_id, email=email)
    return user


def get_user(email: str):
    db = get_mongo_db()
    collection = db["users"]
    if not email:
        raise GraphQLError(
            message="No email has been provided",
            extensions={
                "code": "BAD_REQUEST",
            },
        )
    user = collection.find_one({"email": email})
    if not user:
        return None
    return user


def get_user_by_id(user_id: str) -> User:
    objInstance = ObjectId(user_id)
    db = get_mongo_db()
    collection = db["users"]
    if not user_id:
        raise GraphQLError(
            message="No such user exists",
            extensions={
                "code": "BAD_REQUEST",
            },
        )
    user = collection.find_one({"_id": objInstance})
    if not user:
        return None  # User not found
    #
    return User(id=user_id, email=user.get("email"))


def update_user(user: User):
    ...


def delete_user(uid: List[str]):
    # Delete a user or list of user
    ...
