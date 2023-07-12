# -*- coding: utf-8 -*-
import logging
from typing import Any

import strawberry
from expense.schema import (
    ExpenseInput,
    Response,
    Success,
    ExpenseListRespones,
    ExpenseResponse,
)
from expense.services import TxExpenseSevice
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
    tx_service = TxExpenseSevice()
    await tx_service.process_and_save_tx(data=data)
    # expense_data = data.to_dict(orient="records")

    # response = bulk_upload_data(
    #     collection="expense", data=expense_data, ordered=False
    # )

    return Success(message="File processed successfully.")


@strawberry.field(permission_classes=[IsAuthenticated])
async def get_expense_totals(
    self, info: Info, frequency: str, period: int
) -> ExpenseListRespones:
    collection = "normal_tx"
    tx_service = TxExpenseSevice()
    if "monthly" == frequency:
        result = tx_service.tx_totals_by_months(
            collection=collection, year=period, user_id=info.context.user.id
        )
    else:
        result = ExpenseListRespones()

    return ExpenseListRespones(
        data=[
            ExpenseResponse(
                _id=x.get("_id"),
                total_paid_in=x.get("total_paid_in"),
                total_paid_out=x.get("total_paid_out"),
            )
            for x in result
        ]
    )
