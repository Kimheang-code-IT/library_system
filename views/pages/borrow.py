# views/pages/borrow.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BorrowPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Borrow/Return interface goes here"))
