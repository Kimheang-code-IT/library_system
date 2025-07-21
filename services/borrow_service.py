# services/borrow_service.py

import oracledb
from db_connection import get_connection
from models.borrow_transaction import BorrowTransaction

class BorrowService:
    def __init__(self):
        self.conn = get_connection()

    def checkout_book(
        self,
        student_id: int,
        book_id: int,
        term_id: int,
        due_days: int = 14
    ) -> int:
        cur = self.conn.cursor()
        txn_var = cur.var(oracledb.NUMBER)
        cur.callproc(
            "borrow_pkg.checkout_book",
            [student_id, book_id, term_id, due_days, txn_var]
        )
        cur.close()
        return int(txn_var.getvalue())

    def return_book(self, txn_id: int) -> None:
        cur = self.conn.cursor()
        cur.callproc("borrow_pkg.return_book", [txn_id])
        cur.close()

    def list_borrowed(self, student_id: int) -> list[BorrowTransaction]:
        cur    = self.conn.cursor()
        out_cur = self.conn.cursor()
        cur.callproc("borrow_pkg.list_borrowed", [student_id, out_cur])
        txns = []
        for txn_id, book_id, borrow_date, due_date, return_date, status in out_cur:
            txns.append(BorrowTransaction(
                txn_id=int(txn_id),
                book_id=int(book_id),
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date,
                status=status
            ))
        out_cur.close()
        cur.close()
        return txns
