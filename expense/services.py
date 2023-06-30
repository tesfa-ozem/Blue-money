# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any


class ExpenseService(ABC):
    @abstractmethod
    def calculate_totals_by_periods(
        self, start_date: datetime, end_date: datetime, **kwargs
    ) -> List[Dict[str, int]]:
        pass

    @abstractmethod
    def find_highest_account(
        self, start_date: datetime, end_date: datetime, **kwargs
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_least_account(
        self, start_date: datetime, end_date: datetime, **kwargs
    ) -> List[Dict[str, Any]]:
        pass
