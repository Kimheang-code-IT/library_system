# test_connection.py

from db_connection import get_connection

def test():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello, Oracle!' FROM dual")
    print(cur.fetchone()[0])

if __name__ == "__main__":
    test()
