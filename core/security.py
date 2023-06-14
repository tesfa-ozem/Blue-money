# -*- coding: utf-8 -*-
from datetime import datetime

import jwt
from config import (
    ACCESS_TOKEN_EXPIRY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRY,
    SECRET_KEY,
)
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


def generate_access_token(user_id: str) -> str:
    payload = {"user_id": user_id, "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRY}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token(user_id: str) -> str:
    payload = {"user_id": user_id, "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRY}
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
        raise Exception("Invalid or expired refresh token")
    except jwt.DecodeError:
        raise Exception("Invalid refresh token")
    except Exception as e:
        raise Exception(str(e))


def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        # Handle token expiration error
        raise Exception("Invalid or expired access token")
    except jwt.InvalidTokenError:
        # Handle invalid token error
        raise Exception("Invalid access token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
