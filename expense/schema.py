# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from typing import List, Optional

import strawberry
from strawberry.file_uploads import Upload


# Expense Category
@strawberry.type
class ExpenseCategory:
    category_id: str
    name: str


# Expense Frequency Enum
@strawberry.enum
class ExpenseFrequency(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


# Expense
@strawberry.type
class Expense:
    expense_id: str
    category_id: str
    description: str
    reference: str
    amount: float
    date: datetime
    frequency: ExpenseFrequency
    custom_period_start_date: Optional[datetime] = None
    custom_period_end_date: Optional[datetime] = None


@strawberry.input
class ExpenseInput:
    description: str
    reference: str
    category: str
    amount: float
    date: datetime
    frequency: ExpenseFrequency
    custom_period_start_date: Optional[datetime] = None
    custom_period_end_date: Optional[datetime] = None


@strawberry.input
class ExpenseFileInput:
    files: List[Upload]


@strawberry.type
class Success:
    message: str
    response: str


@strawberry.type
class Error:
    message: str


Response = strawberry.union("Response", (Success, Error))
