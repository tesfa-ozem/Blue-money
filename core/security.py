# -*- coding: utf-8 -*-
from datetime import datetime

import jwt
from auth.schema import User
from config import (
    ACCESS_TOKEN_EXPIRY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRY,
    SECRET_KEY,
)
from db.services import get_user_by_id
from passlib.context import CryptContext
from graphql import GraphQLError


pwd_context = CryptContext(schemes=["bcrypt"])


def generate_access_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRY,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRY,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def refresh_access_token(refresh_token: str) -> str:
    try:
        # Verify the refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Generate a new access token
        access_token = generate_access_token(user_id)
        print(access_token)

        # Return the new access token to the client
        return access_token
    except jwt.ExpiredSignatureError:
        # Handle expired or invalid refresh tokens
        raise GraphQLError(
            message="Refresh token has expired",
            extensions={
                "code": "FORBIDDEN",
            },
        )
    except jwt.DecodeError:
        raise GraphQLError(
            message="Refresh token is invalid",
            extensions={
                "code": "FORBIDDEN",
            },
        )
    except Exception as e:
        raise Exception(str(e))


def decode_jwt_token(token: str) -> dict:
    try:
        token = token.replace("Bearer ", "", 1)
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        # Handle token expiration error
        raise GraphQLError(
            message="Access token has expired",
            extensions={
                "code": "FORBIDDEN",
            },
        )
    except jwt.InvalidTokenError:
        # Handle invalid token error
        raise GraphQLError(
            message="Access token is invalid",
            extensions={
                "code": "FORBIDDEN",
            },
        )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authorize(token: str) -> User | None:
    if not token:
        raise GraphQLError(
            message="Token not provided",
            extensions={
                "code": "FORBIDDEN",
            },
        )
    try:
        token = token.replace("Bearer ", "", 1)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token.get("user_id")
        # Fetch user from database based on user_id
        user = get_user_by_id(user_id)
        return user
    except jwt.ExpiredSignatureError:
        # Handle token expiration error
        raise GraphQLError(
            message="Access token has expired",
            extensions={
                "code": "FORBIDDEN",
            },
        )
    except jwt.InvalidTokenError:
        # Handle invalid token error
        raise GraphQLError(
            message="Access token is invalid",
            extensions={
                "code": "FORBIDDEN",
            },
        )
