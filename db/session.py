# -*- coding: utf-8 -*-
from config import MONGO_DATABASE, MONGO_HOST, MONGO_PORT
from pymongo import MongoClient


def get_mongo_client():
    # client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    return client


def get_mongo_db():
    client = get_mongo_client()
    db = client[MONGO_DATABASE]
    return db
