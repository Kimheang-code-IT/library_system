# models/book.py

from dataclasses import dataclass

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    isbn: str
    category_id: int
    total_copies: int
    available_copies: int
