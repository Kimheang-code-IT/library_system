# views/pages/books.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BookPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Book management goes here"))
