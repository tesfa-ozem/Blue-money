# -*- coding: utf-8 -*-
from api.schema import schema
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


app = FastAPI()

graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")
