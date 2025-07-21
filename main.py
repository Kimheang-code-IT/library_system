# main.py
import sys
from PyQt6.QtWidgets import QApplication
from controllers.login import LoginWindow

def main():
    app = QApplication(sys.argv)
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
