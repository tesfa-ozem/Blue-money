# -*- coding: utf-8 -*-
from typing import List

import strawberry
from expense.schema import ExpenseInput, Response, Success
from strawberry.file_uploads import Upload


@strawberry.mutation
def create_expense(expense: ExpenseInput) -> Response:
    ...


@strawberry.mutation
async def read_expense_files(self, file: Upload) -> Response:
    file_content = await file.read()
    decoded_content = file_content.decode("utf-8")
    print(file)

    return Success(response=decoded_content, message="success")


@strawberry.mutation
def bulk_create_expense(expense: List[ExpenseInput]) -> Response:
    ...


@strawberry.mutation
def update_expense() -> Response:
    ...


@strawberry.mutation
def delete_expense() -> Response:
    ...
