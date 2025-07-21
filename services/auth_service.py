# services/auth_service.py

import hashlib
import oracledb
from db_connection import get_connection
from models.user import User

class AuthService:
    def __init__(self):
        self.conn = get_connection()

    def login(self, username: str, password: str) -> User | None:
        # 1) Compute the raw SHA1 digest
        pw_hash = hashlib.sha1(password.encode('utf-8')).digest()

        # 2) Call the PL/SQL function
        cur = self.conn.cursor()
        user_id = cur.callfunc(
            "auth_pkg.login_user",
            oracledb.NUMBER,
            [username, pw_hash]
        )

        if user_id:
            # 3) Fetch the user's role
            cur.execute(
                "SELECT role FROM users WHERE user_id = :id",
                id=int(user_id)
            )
            role = cur.fetchone()[0]
            return User(user_id=int(user_id), username=username, role=role)

        return None
