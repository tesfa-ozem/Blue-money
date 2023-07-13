# -*- coding: utf-8 -*-
import strawberry
from auth.schema import AccessToken, LoginResult, LoginSuccess, User
from core.security import (
    generate_access_token,
    generate_refresh_token,
    refresh_access_token,
    verify_password,
)
from core.utility import check_password_strength
from db.services import add_user_service, get_user
from graphql import GraphQLError


@strawberry.mutation
def login(email: str, password: str) -> LoginResult:
    # Your domain-specific authentication logic would go here
    user = get_user(email)
    if user is None:
        return GraphQLError(
            message="email not valid",
            extensions={
                "error_code": 404,
            },
        )

    is_authenticated = verify_password(password, user.get("password"))
    print(user)
    if not is_authenticated:
        raise GraphQLError(
            message="email or password is incorrect",
            extensions={
                "error_code": 401,
            },
        )
    user_id = str(user["_id"])
    access_token = generate_access_token(user_id)
    refresh_token = generate_refresh_token(user_id)

    # user_object = User(id=user_id, email=user.get(email))
    login_user = User(id=user_id, email=user.get("email"))
    return LoginSuccess(
        user=login_user, access_token=access_token, refresh_token=refresh_token
    )


@strawberry.mutation
def refresh_token(refresh_token: str) -> AccessToken:
    try:
        access_token = refresh_access_token(refresh_token)
        return AccessToken(access_token=access_token)
    except Exception as e:
        raise GraphQLError(
            message=str(e),
            extensions={"error_code": 401, "error_type": "auth_error"},
        )


@strawberry.mutation
def add_user(email: str, password: str) -> User:
    is_strong, message = check_password_strength(password)
    if not is_strong:
        raise GraphQLError(
            message=message,
            extensions={
                "error_code": 400,
            },
        )
    inserted_user = add_user_service(email, password)
    return inserted_user
