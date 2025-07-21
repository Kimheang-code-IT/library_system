# views/admin_dashboard.py

from views.base_dashboard import BaseDashboard
from views.pages.home        import HomePage
from views.pages.categories  import CategoryPage
from views.pages.books       import BookPage
from views.pages.borrow      import BorrowPage

class AdminDashboard(BaseDashboard):
    def __init__(self, user):
        menu = ["Home", "Categories", "Books", "Borrow"]
        pages = [HomePage(), CategoryPage(), BookPage(), BorrowPage()]
        super().__init__(user, menu, pages)
