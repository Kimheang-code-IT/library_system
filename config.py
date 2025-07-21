# config.py

import os

# Credentials for your Library_System schema
DB_USER = os.getenv("DB_USER", "LIBRARY_SYSTEM")
DB_PWD  = os.getenv("DB_PWD",  "123")

# Connection details matching your SQL Developer “free” SID entry
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 1521))
DB_SID  = os.getenv("DB_SID",  "free")
