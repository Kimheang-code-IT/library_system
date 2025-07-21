# quick_test_borrow.py

from services.auth_service     import AuthService
from services.category_service import CategoryService
from services.book_service     import BookService
from services.borrow_service   import BorrowService
from db_connection             import get_connection

if __name__ == "__main__":
    # 1) Log in as admin (to upload a demo book)
    admin = AuthService().login("admin", "adminpass")
    assert admin, "Admin login failed!"

    # 2) Pick a real category and term
    category = CategoryService().list_categories()[0]

    # Fetch a term_id directly
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT term_id FROM terms FETCH FIRST 1 ROWS ONLY")
    term_id = cur.fetchone()[0]
    cur.close()

    # 3) Add a demo book
    book_id = BookService().add_book(
        title="BorrowDemo",
        author="Bob Example",
        isbn="9876543210",
        category_id=category.category_id,
        total_copies=1,
        pdf_bytes=b"%PDF-1.4 demo",
        cover_bytes=b"\x89PNG demo",
        uploaded_by=admin.user_id
    )
    print("Demo book_id:", book_id)

    # 4) Log in as student1 to get users.user_id
    student_user = AuthService().login("student1", "studentpass")
    if not student_user:
        raise RuntimeError("student1 login failed—did you seed the student?")

    # === THIS IS THE FIX ===
    # 5) Lookup the actual students.student_id for that user
    cur = conn.cursor()
    cur.execute(
        "SELECT student_id FROM students WHERE user_id = :u",
        u=student_user.user_id
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError("No students record found for that user_id")
    student_id = row[0]
    cur.close()

    borrow_svc = BorrowService()

    # 6) Checkout
    txn_id = borrow_svc.checkout_book(student_id, book_id, term_id)
    print("Checked out txn_id:", txn_id)

    # 7) List loans
    print("Active loans:")
    for txn in borrow_svc.list_borrowed(student_id):
        print(" ", txn)

    # 8) Return
    borrow_svc.return_book(txn_id)
    print("Returned txn_id:", txn_id)

    # 9) List again
    print("Loans after return:")
    for txn in borrow_svc.list_borrowed(student_id):
        print(" ", txn)
