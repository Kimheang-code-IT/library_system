# controllers/login.py

from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit,
    QPushButton, QMessageBox
)
from db_connection import get_connection
from models.user   import User
from views.admin_dashboard   import AdminDashboard
from views.student_dashboard import StudentDashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library System — Login")
        self.setFixedSize(360, 160)

        form = QFormLayout(self)
        form.setContentsMargins(20, 20, 20, 20)
        form.setSpacing(12)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your username")
        form.addRow("Username:", self.user_input)

        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setPlaceholderText("Enter your password (123)")
        form.addRow("Password:", self.pw_input)

        self.login_btn = QPushButton("Log In")
        form.addRow(self.login_btn)

        self.login_btn.clicked.connect(self.attempt_login)
        self.pw_input.returnPressed.connect(self.attempt_login)

    def attempt_login(self):
        username = self.user_input.text().strip()
        password = self.pw_input.text()

        # 1) Validate inputs
        if not username or not password:
            QMessageBox.warning(self, "Missing Credentials", "Please enter both username and password.")
            return

        # 2) Static password check
        if password != "123":
            QMessageBox.critical(self, "Login Failed", "Password must be '123'.")
            return

        # 3) Lookup the user in the database
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "SELECT user_id, role FROM users WHERE LOWER(username)=:u",
            u=username.lower()
        )
        row = cur.fetchone()
        cur.close()

        if not row:
            QMessageBox.critical(self, "Login Failed", f"No user '{username}' found.")
            return

        user_id, role = row
        user = User(user_id=user_id, username=username, role=role)

        # 4) Route to the appropriate dashboard
        if role.upper() == "ADMIN":
            self.dashboard = AdminDashboard(user)
        else:
            self.dashboard = StudentDashboard(user)

        self.dashboard.show()
        self.close()
