# -*- coding: utf-8 -*-
import strawberry
from auth.resolvers import add_user, login, refresh_token
from auth.schema import LoginResult


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> str:
        return "A user"

    # Define your GraphQL queries here


@strawberry.type
class Mutation:
    login: LoginResult = login
    register = add_user
    refreshToken = refresh_token


schema = strawberry.Schema(query=Query, mutation=Mutation)
