# Library System

A library management application built with Python against an Oracle database,
covering the catalogue, categories, users and the borrow/return workflow.

This is the more developed sibling of the `Oracle_Project-Library` assignment,
adding a service layer, SQL scripts and quick smoke tests.

## Architecture

MVC with an added service layer and shared utilities.

```text
main.py                  Entry point
config.py                Configuration
db_connection.py         Oracle connection handling
models/                  Data access layer
  book.py
  category.py
  user.py
  borrow_transaction.py
controllers/             Request handling
services/                Business rules shared across controllers
views/                   Presentation layer (admin and student dashboards)
sql/                     Schema and seed scripts
utils/                   Shared helpers
resources/               Icons and styles
```

## Setup

1. Apply the SQL scripts in `sql/`.
2. Update `config.py` with your Oracle connection details.
3. Run:

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## Smoke tests

Handy scripts for verifying each area quickly:

```bash
python test_connection.py
python test_seed_data.py
python quick_test_auth.py
python quick_test_book.py
python quick_test_borrow.py
python quick_test_category.py
```

## Features

- Book catalogue with categories
- Borrowing and return workflow
- Borrow transaction history
- User and authentication handling
- Separate admin and student dashboards
