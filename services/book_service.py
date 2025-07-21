# services/book_service.py

import oracledb
from db_connection import get_connection
from models.book import Book

class BookService:
    def __init__(self):
        self.conn = get_connection()

    def list_books(self) -> list[Book]:
        cur = self.conn.cursor()
        out_cur = self.conn.cursor()
        cur.callproc("book_pkg.list_books", [out_cur])
        books = [
            Book(
                book_id=bid,
                title=title,
                author=author,
                isbn=isbn,
                category_id=cat,
                total_copies=tot,
                available_copies=avail
            )
            for bid, title, author, isbn, cat, tot, avail in out_cur
        ]
        out_cur.close()
        cur.close()
        return books

    def add_book(
        self,
        title: str,
        author: str,
        isbn: str,
        category_id: int,
        total_copies: int,
        pdf_bytes: bytes,
        cover_bytes: bytes,
        uploaded_by: int
    ) -> int:
        cur = self.conn.cursor()
        # Prepare LOB binding
        pdf_blob = self.conn.createlob(oracledb.DB_TYPE_BLOB)
        pdf_blob.write(pdf_bytes)
        cover_blob = self.conn.createlob(oracledb.DB_TYPE_BLOB)
        cover_blob.write(cover_bytes)

        book_id_var = cur.var(oracledb.NUMBER)
        cur.callproc(
            "book_pkg.add_book",
            [
                title, author, isbn, category_id,
                total_copies, pdf_blob, cover_blob,
                uploaded_by, book_id_var
            ]
        )
        cur.close()
        return int(book_id_var.getvalue())

    def remove_book(self, book_id: int) -> None:
        cur = self.conn.cursor()
        cur.callproc("book_pkg.remove_book", [book_id])
        cur.close()

    def get_pdf(self, book_id: int) -> bytes:
        cur = self.conn.cursor()
        lob = cur.callfunc("book_pkg.get_pdf", oracledb.DB_TYPE_BLOB, [book_id])
        data = lob.read()
        cur.close()
        return data

    def get_cover(self, book_id: int) -> bytes:
        cur = self.conn.cursor()
        lob = cur.callfunc("book_pkg.get_cover", oracledb.DB_TYPE_BLOB, [book_id])
        data = lob.read()
        cur.close()
        return data
