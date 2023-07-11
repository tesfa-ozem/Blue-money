# -*- coding: utf-8 -*-
import pytest
from config import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient
from expense.services import TxExpenseSevice

# Assuming you have a MongoDB connection setup already
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client["test_db"]


@pytest.fixture(scope="module")
def setup_collection():
    # Perform any necessary setup before running the tests
    collection = db["normal_tx"]

    # Insert some test data
    test_data = [
        {"time": "2022-01-01 10:00:00"},
        {"time": "2022-02-01 11:00:00"},
        {"time": "2023-01-01 12:00:00"},
        {"time": "2023-02-01 13:00:00"},
    ]
    collection.insert_many(test_data)

    yield collection

    # Clean up after running the tests
    collection.delete_many({})


def test_get_years(setup_collection):
    collection = db["normal_tx"]
    repo = TxExpenseSevice()
    # Call the function being tested
    result = repo.get_years(collection=collection)

    # Assert the expected result
    assert isinstance(result, list)
    assert len(result) == 2
    assert "2022" in result
    assert "2023" in result
