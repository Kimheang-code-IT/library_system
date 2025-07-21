# views/pages/home.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Welcome to the Home Page"))
