# -*- coding: utf-8 -*-
import logging
from typing import Any, List

import strawberry
from db.session import get_mongo_db
from expense.schema import Error, ExpenseInput, Response, Success
from file_processing.file_processing import (
    CSVFileReaderFactory,
    FileProcessor,
    PDFFileReaderFactory,
    XLSXFileReaderFactory,
)
from file_processing.file_utilities import decrypt_pdf
from strawberry.file_uploads import Upload
from strawberry.permission import BasePermission
from strawberry.types import Info
from PyPDF2 import PdfReader
import io
import pymongo.errors


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        if info.context.user:
            return True
        return False


logger = logging.getLogger(__name__)


@strawberry.mutation
def create_expense(expense: ExpenseInput) -> Response:
    ...


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def read_expense_files(self, info: Info, file: Upload) -> Response:
    user_id = info.context.user.id
    # Validate file type
    allowed_file_types = [
        "text/csv",
        "application/vnd.ms-excel",
        "application/pdf",
    ]
    if file.content_type not in allowed_file_types:
        return Error(
            message="Invalid file type. Only CSV \
            and XLSX files are accepted."
        )

    # Validate file size
    max_file_size = 5 * 1024 * 1024  # 2 MB
    if file.size > max_file_size:
        return Error(message="File size exceeds the limit of 2MB.")

    if file.content_type == "application/pdf":
        factory = PDFFileReaderFactory()
    elif file.content_type == "text/csv":
        factory = CSVFileReaderFactory()
    elif file.content_type == "application/vnd.ms-excel":
        factory = XLSXFileReaderFactory()
    else:
        raise ValueError("Unsupported file type.")

    try:
        # Read the contents of the Upload as bytes
        file_bytes = await file.read()

        # Check if the PDF is encrypted
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        if pdf_reader.is_encrypted:
            # Decrypt the PDF using the provided password
            file_bytes = await decrypt_pdf(pdf_reader, "474833")

    except Exception as e:
        logger.error(e)
        return Error(message="Failed to read file.")

    processor = FileProcessor(factory)
    data = processor.process_file(file_bytes)

    if data is None:
        return Error(message="Failed to process file.")

    data["user_id"] = user_id
    expense_data = data.to_dict(orient="records")
    # data.to_csv('./expense.csv')

    db = get_mongo_db()
    collection = db["expense"]
    try:
        collection.insert_many(expense_data, ordered=False)
    except pymongo.errors.BulkWriteError as e:
        # Handle the duplicate key error
        for error in e.details["writeErrors"]:
            if error["code"] == 11000:
                # Duplicate key error
                # Handle or log the error as needed
                print(f"Duplicate key error: {error['errmsg']}")
            else:
                # Other types of errors
                # Handle or log the error as needed
                print(f"Other error: {error['errmsg']}")

    return Success(message="File processed successfully.")


@strawberry.mutation
def bulk_create_expense(expense: List[ExpenseInput]) -> Response:
    ...


@strawberry.mutation
def update_expense() -> Response:
    ...


@strawberry.mutation
def delete_expense() -> Response:
    ...


# Background task


def save_expense():
    ...
