# -*- coding: utf-8 -*-
from typing import List, Dict
import pymongo.errors
from db.session import get_mongo_db
import asyncio
from dataclasses import dataclass


@dataclass
class TxExpenseSevice:
    def filter_normal_tx(self, df) -> List[Dict]:
        """
        Filters normal transactions from a dataframe
        """
        try:
            exclude = [
                "Withdrawal Charge",
                "Pay Bill Charge",
                "Pay Merchant Charge",
                "Customer Transfer of Funds Charge",
                "OverDraft of Credit Party",
            ]

            filtered_df = df[
                ~df["details"].isin(exclude)
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
            include = [
                "Withdrawal Charge",
                "Pay Bill Charge",
                "Pay Merchant Charge",
                "Customer Transfer of Funds Charge",
            ]

            filtered_df = df[df["details"].isin(include)]

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
            include = ["OverDraft of Credit Party"]

            filtered_df = df[df["details"].isin(include)]

            # Convert the filtered dataframe to a list of dictionaries
            transactions = filtered_df.to_dict("records")

            return transactions

        except KeyError as e:
            print(f"KeyError occurred: {str(e)}")
            return []

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    async def save_normal_tx(
        self, collection: str, data: Dict, **config
    ) -> None:
        db = get_mongo_db()
        collection = db[collection]
        try:
            index_info = collection.index_information()
            if "reference_1" not in index_info:
                collection.create_index(
                    [("reference", 1)], unique=True, sparse=True
                )
            collection.insert_many(data, **config)
        except pymongo.errors.BulkWriteError as e:
            write_errors = e.details.get("writeErrors", [])
            duplicates = [x.get("op") for x in write_errors]
            collection = db["unsorted_tx"]
            collection.insert_many(duplicates, **config)
        except Exception as error:
            # Handle any other exceptions that might occur
            # Log the error or perform any other error handling actions
            raise Exception(f"An unexpected error occurred, {error}")

    async def save_charge_tx(
        self, collection: str, data: Dict, **config
    ) -> None:
        db = get_mongo_db()
        collection = db[collection]
        try:
            index_info = collection.index_information()
            if "reference_1" not in index_info:
                collection.create_index(
                    [("reference", 1)], unique=True, sparse=True
                )
            collection.insert_many(data, **config)
        except pymongo.errors.BulkWriteError as e:
            write_errors = e.details.get("writeErrors", [])
            duplicates = [x.get("op") for x in write_errors]
            collection = db["unsorted_tx"]
            collection.insert_many(duplicates, **config)
        except Exception as error:
            # Handle any other exceptions that might occur
            # Log the error or perform any other error handling actions
            raise Exception(f"An unexpected error occurred, {error}")

    async def save_overdraft_tx(
        self, collection: str, data: Dict, **config
    ) -> None:
        db = get_mongo_db()
        collection = db[collection]
        try:
            index_info = collection.index_information()
            if "reference_1" not in index_info:
                collection.create_index(
                    [("reference", 1)], unique=True, sparse=True
                )
            collection.insert_many(data, **config)
        except pymongo.errors.BulkWriteError as e:
            write_errors = e.details.get("writeErrors", [])
            duplicates = [x.get("op") for x in write_errors]
            collection = db["unsorted_tx"]
            collection.insert_many(duplicates, **config)
        except Exception as error:
            # Handle any other exceptions that might occur
            # Log the error or perform any other error handling actions
            raise Exception(f"An unexpected error occurred, {error}")

    async def process_and_save_tx(self, data):
        """
        process the dataframe and save to the database
        """
        try:
            normal_tx = self.filter_normal_tx(data)
            charge_tx = self.filter_charge_tx(data)
            over_darft_tx = self.filter_overdraft_tx(data)

            tasks = [
                asyncio.create_task(
                    self.save_normal_tx(
                        collection="normal_tx", data=normal_tx, ordered=False
                    )
                ),
                asyncio.create_task(
                    self.save_charge_tx(
                        collection="charge_tx", data=charge_tx, ordered=False
                    )
                ),
                asyncio.create_task(
                    self.save_overdraft_tx(
                        collection="overdraft_tx",
                        data=over_darft_tx,
                        ordered=False,
                    )
                ),
            ]
            results = await asyncio.gather(*tasks)
            return results
        except Exception as e:
            raise Exception(str(e))
