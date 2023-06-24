# -*- coding: utf-8 -*-
from functools import cached_property

from api.schema import schema
from auth.schema import User
from core.security import authorize
from fastapi import FastAPI
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType


class Context(BaseContext):
    @cached_property
    def user(self) -> User | None:
        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", None)
        return authorize(authorization)


Info = _Info[Context, RootValueType]


async def get_context() -> Context:
    return Context()


app = FastAPI()

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(graphql_app, prefix="/graphql")
