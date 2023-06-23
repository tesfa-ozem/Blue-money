# -*- coding: utf-8 -*-
import logging
from typing import List

import strawberry
from expense.schema import Error, ExpenseInput, Response, Success
from file_processing.file_processing import (
    CSVFileReaderFactory,
    FileProcessor,
    PDFFileReaderFactory,
    XLSXFileReaderFactory,
)
from strawberry.file_uploads import Upload


logger = logging.getLogger(__name__)


@strawberry.mutation
def create_expense(expense: ExpenseInput) -> Response:
    ...


@strawberry.mutation
async def read_expense_files(self, file: Upload) -> Response:
    # Validate file type
    allowed_file_types = ["text/csv", "application/vnd.ms-excel", "application/pdf"]
    if file.content_type not in allowed_file_types:
        return Error(message="Invalid file type. Only CSV and XLSX files are accepted.")

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

    # Save expenses
    # try:
    #     await save_expense(data)
    # except Exception as e:
    #     logger.error(e)
    #     return Error(message="Failed to save expenses.")

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
