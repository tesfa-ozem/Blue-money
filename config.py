# -*- coding: utf-8 -*-
from datetime import timedelta

from decouple import Config, RepositoryEnv


# Create a Config object and load variables from the .env file
config = Config(RepositoryEnv("./.env"))
# Define configuration variables
MONGO_HOST = config("MONGO_HOST", default="localhost")
MONGO_PORT = config("MONGO_PORT", default=27017, cast=int)
MONGO_DATABASE = config("MONGO_DATABASE", default="bv-auth-db")
MONGO_URI = config("MONGO_URI", default="")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = timedelta(minutes=config("ACCESS_TOKEN_EXPIRY", cast=int))
REFRESH_TOKEN_EXPIRY = timedelta(days=config("REFRESH_TOKEN_EXPIRY", cast=int))
