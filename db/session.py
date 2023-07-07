# -*- coding: utf-8 -*-
from config import MONGO_DATABASE, MONGO_URI
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_mongo_client():
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    return client


def get_mongo_db():
    client = get_mongo_client()
    db = client[MONGO_DATABASE]
    return db
