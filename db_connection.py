# db_connection.py

import oracledb
from config import DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_SID


_conn = None

def get_connection():
    global _conn
    if _conn is None:
        # Build a DSN using the SID, since your listener registered "free"
        dsn = oracledb.makedsn(DB_HOST, DB_PORT, sid=DB_SID)
        _conn = oracledb.connect(
            user=DB_USER,
            password=DB_PWD,
            dsn=dsn
        )
    return _conn
