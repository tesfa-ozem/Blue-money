# -*- coding: utf-8 -*-
import pytest
from config import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient
from expense.services import TxExpenseSevice
import json
import os

# Assuming you have a MongoDB connection setup already
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client["test_db"]


@pytest.fixture(scope="module")
def setup_collection():
    # Perform any necessary setup before running the tests
    collection = db["normal_tx"]

    # Insert some test data
    file_path = os.path.join(os.path.dirname(__file__), "test_data.json")
    f = open(file_path)
    test_data = json.loads(f.read())
    f.close()
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
    # assert len(result) == 2
    assert "2022" in result
    assert "2023" in result


def test_month_aggregation(setup_collection):
    collection = "normal_tx"
    repo = TxExpenseSevice()
    # Call the function being tested

    result = repo.tx_totals_by_months(
        collection=collection, year=2022, user_id="6497037713a21a1325296aae"
    )
    print(result)

    assert len(result) == 12
    assert result[0].get("total_paid_in") == 139_742
    assert result[0].get("total_paid_out") == -147_631
