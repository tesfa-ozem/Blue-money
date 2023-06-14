# -*- coding: utf-8 -*-
import strawberry


@strawberry.type
class User:
    id: str
    email: str

    # Add any other fields related to the user


# Define your authentication token model


@strawberry.type
class LoginSuccess:
    user: User
    access_token: str
    refresh_token: str


@strawberry.type
class AccessToken:
    access_token: str


@strawberry.type
class LoginError:
    message: str


LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))
