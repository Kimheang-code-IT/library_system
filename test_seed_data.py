# test_seed_data.py

from db_connection import get_connection

def main():
    conn = get_connection()
    cur = conn.cursor()

    print("USERS:")
    cur.execute("SELECT username, role, status FROM users")
    for row in cur.fetchall():
        print(" ", row)

    print("\nTERMS:")
    cur.execute("SELECT term_id, name, start_date, end_date FROM terms ORDER BY term_id")
    for row in cur.fetchall():
        print(" ", row)

    print("\nCATEGORIES:")
    cur.execute("SELECT category_id, name FROM categories")
    for row in cur.fetchall():
        print(" ", row)

if __name__ == "__main__":
    main()
