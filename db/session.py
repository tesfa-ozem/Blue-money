# -*- coding: utf-8 -*-
from config import (
    MONGO_DATABASE,
    MONGO_HOST,
    MONGO_PORT,
    ENVIRONMENT,
    MONGO_URI,
)
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from graphql import GraphQLError


def get_mongo_client():
    try:
        if ENVIRONMENT == "development":
            # client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
            client = MongoClient(
                MONGO_HOST,
                MONGO_PORT,
            )
        if ENVIRONMENT == "test":
            client = MongoClient(
                MONGO_URI,
                server_api=ServerApi("1"),
            )
        client.server_info()
        return client
    except errors.AutoReconnect as e:
        raise GraphQLError(
            message=f"Database connection refused - {str(e)}",
            extensions={
                "code": "INTERNAL_SERVER_ERROR",
            },
        )


def get_mongo_db():
    client = get_mongo_client()
    db = client[MONGO_DATABASE]
    return db
