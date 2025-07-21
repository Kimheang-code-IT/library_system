# views/pages/categories.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CategoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Categories will go here"))
