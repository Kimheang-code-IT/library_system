# quick_test_category.py

from services.category_service import CategoryService

if __name__ == "__main__":
    svc = CategoryService()

    print("Existing categories:")
    for cat in svc.list_categories():
        print(" ", cat)

    print("\nAdding 'TestCat'…")
    svc.add_category("TestCat", "A test category")
    for cat in svc.list_categories():
        print(" ", cat)

    print("\nUpdating 'TestCat'…")
    # find its ID
    test = next(c for c in svc.list_categories() if c.name == "TestCat")
    svc.edit_category(test.category_id, "TestCat2", "Renamed test category")
    for cat in svc.list_categories():
        print(" ", cat)

    print("\nRemoving 'TestCat2'…")
    svc.remove_category(test.category_id)
    for cat in svc.list_categories():
        print(" ", cat)
