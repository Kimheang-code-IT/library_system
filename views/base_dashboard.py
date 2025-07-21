from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QListWidget,
    QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt

class BaseDashboard(QWidget):
    """
    Base class for Admin and Student dashboards.
    Left: sidebar (QListWidget).
    Top: header with search bar.
    Main content: QStackedWidget inside a scroll area.
    """
    def __init__(self, user, menu_items: list[str], pages: list[QWidget]):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"{self.user.username} Dashboard")
        self.menu_items = menu_items
        self.pages = pages
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItems(self.menu_items)
        self.sidebar.currentRowChanged.connect(self._on_menu_changed)
        self.sidebar.setFixedWidth(200)
        main_layout.addWidget(self.sidebar)

        # Container for header and content
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Header with search bar
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.addWidget(QLabel("Search:"), alignment=Qt.AlignmentFlag.AlignLeft)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search ...")
        header_layout.addWidget(self.search_input)
        container_layout.addWidget(header)

        # Stacked pages inside a scrollable area
        self.stack = QStackedWidget()
        for page in self.pages:
            self.stack.addWidget(page)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.stack)
        container_layout.addWidget(scroll)

        main_layout.addWidget(container)

        # Initialize at first page
        self.sidebar.setCurrentRow(0)

    def _on_menu_changed(self, index: int):
        self.stack.setCurrentIndex(index)

# Example usage in views/admin_dashboard.py:
# from views.base_dashboard import BaseDashboard
# from views.pages.home import HomePage
# from views.pages.categories import CategoryPage
# from views.pages.books import BookPage
# from views.pages.borrow import BorrowPage
# menu = ["Home", "Categories", "Books", "Borrow"]
# pages = [HomePage(), CategoryPage(), BookPage(), BorrowPage()]
# class AdminDashboard(BaseDashboard):
#     def __init__(self, user):
#         super().__init__(user, menu, pages)
