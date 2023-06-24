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
from strawberry.file_uploads import Upload
from strawberry.permission import BasePermission
from strawberry.types import Info


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
        file_bytes = await file.read()
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
        collection.insert_many(expense_data)
    except Exception as e:
        print(f"Error: {e}")

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
