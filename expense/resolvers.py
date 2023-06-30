# -*- coding: utf-8 -*-
import logging
from typing import Any, List

import strawberry
from db.services import bulk_upload_data
from expense.schema import ExpenseInput, Response, Success
from file_processing.file_processing import FileProcessor

from file_processing.file_utilities import validate_pdf_file
from strawberry.file_uploads import Upload
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

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
    validate_pdf_file(file)
    file_bytes = await file.read()

    processor = FileProcessor(file.content_type)
    data = await processor.process_file(file_bytes)

    # Add user id to the data
    user_id = info.context.user.id
    data["user_id"] = user_id
    expense_data = data.to_dict(orient="records")

    response = bulk_upload_data(
        collection="expense", data=expense_data, ordered=False
    )
    if response:
        return Success(message="File processed successfully.")
    raise Exception("Failed to Upload data to db")


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
