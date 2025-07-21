# services/category_service.py

import oracledb
from db_connection import get_connection
from models.category import Category

class CategoryService:
    def __init__(self):
        self.conn = get_connection()

    def list_categories(self) -> list[Category]:
        cur = self.conn.cursor()
        out_cur = self.conn.cursor()
        cur.callproc("category_pkg.list_categories", [out_cur])
        cats = []
        for cat_id, name, desc in out_cur:
            cats.append(Category(category_id=cat_id, name=name, description=desc))
        out_cur.close()
        cur.close()
        return cats

    def add_category(self, name: str, description: str) -> None:
        cur = self.conn.cursor()
        cur.callproc("category_pkg.add_category", [name, description])
        cur.close()

    def edit_category(self, category_id: int, name: str, description: str) -> None:
        cur = self.conn.cursor()
        cur.callproc("category_pkg.edit_category", [category_id, name, description])
        cur.close()

    def remove_category(self, category_id: int) -> None:
        cur = self.conn.cursor()
        cur.callproc("category_pkg.remove_category", [category_id])
        cur.close()
