# -*- coding: utf-8 -*-
import strawberry
from auth.resolvers import add_user, login, refresh_token
from auth.schema import LoginResult, User
from expense.schema import ExpenseListRespones
from expense.resolvers import read_expense_files, get_expense_totals
from strawberry.types import Info


@strawberry.type
class Query:
    expenseTotals: ExpenseListRespones = get_expense_totals

    @strawberry.field
    def user(self, info: Info) -> User | None:
        return info.context.user

    # Define your GraphQL queries here


@strawberry.type
class Mutation:
    login: LoginResult = login
    register = add_user
    refreshToken = refresh_token
    readExpenseFiles = read_expense_files


schema = strawberry.Schema(query=Query, mutation=Mutation)
