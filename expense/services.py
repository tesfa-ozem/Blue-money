# -*- coding: utf-8 -*-
from typing import List, Dict
from pymongo.errors import PyMongoError
from dataclasses import dataclass
from db.session import get_mongo_db


@dataclass
class TxExpenseSevice:
    def filter_normal_tx(self, df) -> List[Dict]:
        """
        Filters normal transactions from a dataframe
        """
        try:
            exclude_rows = [
                "Withdrawal Charge",
                "Pay Bill Charge",
                "Pay Merchant Charge",
                "Customer Transfer of Funds Charge",
                "OverDraft of Credit Party",
            ]

            filtered_df = df[
                ~df["details"].isin(exclude_rows)
            ]  # Replace 'column_name' with the actual column name

            # Convert the filtered dataframe to a list of dictionaries
            transactions = filtered_df.to_dict("records")

            return transactions

        except KeyError as e:
            print(f"KeyError occurred: {str(e)}")
            return []

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def filter_charge_tx(self, df) -> List[Dict]:
        """
        Filters charge transactions from a dataframe
        """
        try:
            include_rows = [
                "Withdrawal Charge",
                "Pay Bill Charge",
                "Pay Merchant Charge",
                "Customer Transfer of Funds Charge",
            ]

            filtered_df = df[df["details"].isin(include_rows)]

            # Convert the filtered dataframe to a list of dictionaries
            transactions = filtered_df.to_dict("records")

            return transactions

        except KeyError as e:
            print(f"KeyError occurred: {str(e)}")
            return []

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def filter_overdraft_tx(self, df) -> List[Dict]:
        """
        FIlter out overdraft charges from dataframe
        """
        try:
            include_rows = ["OverDraft of Credit Party"]

            filtered_df = df[df["details"].isin(include_rows)]

            # Convert the filtered dataframe to a list of dictionaries
            transactions = filtered_df.to_dict("records")

            return transactions

        except KeyError as e:
            print(f"KeyError occurred: {str(e)}")
            return []

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def save_normal_tx(self, collection: str, data: Dict, **config) -> None:
        db = get_mongo_db()
        collection = db[collection]
        try:
            index_info = collection.index_information()
            if "reference_1" not in index_info:
                collection.create_index(
                    [("reference", 1)], unique=True, sparse=True
                )
            collection.insert_many(data, **config)
        except PyMongoError as error:
            # Handle PyMongoError (MongoDB related errors)
            # Log the error or perform any other error handling actions

            raise Exception(
                "An error occurred while adding a transactions"
            ) from error
        except Exception as error:
            # Handle any other exceptions that might occur
            # Log the error or perform any other error handling actions
            raise Exception(f"An unexpected error occurred, {error}")

    def save_charge_tx(self, collection: str, data: Dict, **config) -> None:
        db = get_mongo_db()
        collection = db[collection]
        try:
            index_info = collection.index_information()
            if "reference_1" not in index_info:
                collection.create_index(
                    [("reference", 1)], unique=True, sparse=True
                )
            collection.insert_many(data, **config)
        except PyMongoError as error:
            # Handle PyMongoError (MongoDB related errors)
            # Log the error or perform any other error handling actions
            # You can also raise a custom exception or return an error response
            raise Exception(
                "An error occurred while adding a transactions"
            ) from error
        except Exception as error:
            # Handle any other exceptions that might occur
            # Log the error or perform any other error handling actions
            raise Exception(f"An unexpected error occurred, {error}")

    def save_overdraft_tx(self, collection: str, data: Dict, **config) -> None:
        db = get_mongo_db()
        collection = db[collection]
        try:
            index_info = collection.index_information()
            if "reference_1" not in index_info:
                collection.create_index(
                    [("reference", 1)], unique=True, sparse=True
                )
            collection.insert_many(data, **config)
        except PyMongoError as error:
            # Handle PyMongoError (MongoDB related errors)
            # Log the error or perform any other error handling actions
            # You can also raise a custom exception or return an error response
            raise Exception(
                "An error occurred while adding a transactions"
            ) from error
        except Exception as error:
            # Handle any other exceptions that might occur
            # Log the error or perform any other error handling actions
            raise Exception(f"An unexpected error occurred, {error}")
