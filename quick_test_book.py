# quick_test_book.py

from services.category_service import CategoryService
from services.book_service     import BookService
from services.auth_service     import AuthService

if __name__ == "__main__":
    # 1) Log in as admin to get the real user_id
    auth = AuthService()
    admin = auth.login("admin", "adminpass")
    if not admin:
        raise RuntimeError("Admin login failed!")

    # 2) Pick an existing category
    cats = CategoryService().list_categories()
    if not cats:
        raise RuntimeError("No categories found; seed_data failed.")
    category_id = cats[0].category_id

    svc = BookService()

    print("Initial books:")
    for b in svc.list_books():
        print(" ", b)

    print(f"\nAdding demo book under category {category_id} by user {admin.user_id}…")
    new_id = svc.add_book(
        title="Demo Book",
        author="Alice Example",
        isbn="1234567890",
        category_id=category_id,
        total_copies=3,
        pdf_bytes=b"%PDF-1.4 demo pdf content",
        cover_bytes=b"\x89PNG demo cover content",
        uploaded_by=admin.user_id
    )
    print(" New book_id:", new_id)
    for b in svc.list_books():
        print(" ", b)

    print("\nFetching PDF & cover LOBs for demo book…")
    pdf   = svc.get_pdf(new_id)
    cover = svc.get_cover(new_id)
    print(" PDF bytes starts with:", pdf[:10])
    print(" Cover bytes starts with:", cover[:10])

    print("\nRemoving demo book…")
    svc.remove_book(new_id)
    for b in svc.list_books():
        print(" ", b)
