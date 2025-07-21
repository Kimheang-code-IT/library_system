# models/borrow_transaction.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class BorrowTransaction:
    txn_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: str
