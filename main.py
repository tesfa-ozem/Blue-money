# -*- coding: utf-8 -*-
from functools import cached_property

from api.schema import schema
from auth.schema import User
from core.security import authorize
from fastapi import FastAPI
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk


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


sentry_sdk.init(
    dsn="https://eb9f93b5c4f34df1ac6ba7a6deb9928e@o\
    4505535255478272.ingest.sentry.io/4505535259738112",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)


app.include_router(graphql_app, prefix="/graphql")
