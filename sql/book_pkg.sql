-- sql/book_pkg.sql

-- 1) Spec
CREATE OR REPLACE PACKAGE book_pkg AS
  /** 
   * Returns all books (metadata only).
   */
  PROCEDURE list_books(
    p_cursor OUT SYS_REFCURSOR
  );

  /**
   * Adds a new book. Returns the new BOOK_ID.
   * @param p_title
   * @param p_author
   * @param p_isbn
   * @param p_category_id
   * @param p_total_copies
   * @param p_pdf_blob     raw PDF data
   * @param p_cover_blob   raw cover image data
   * @param p_uploaded_by  user_id of uploader
   * @param p_book_id OUT   the new book’s ID
   */
  PROCEDURE add_book(
    p_title        IN VARCHAR2,
    p_author       IN VARCHAR2,
    p_isbn         IN VARCHAR2,
    p_category_id  IN NUMBER,
    p_total_copies IN NUMBER,
    p_pdf_blob     IN BLOB,
    p_cover_blob   IN BLOB,
    p_uploaded_by  IN NUMBER,
    p_book_id      OUT NUMBER
  );

  /**
   * Deletes a book and its LOBs
   */
  PROCEDURE remove_book(
    p_book_id IN NUMBER
  );

  /**
   * Fetches the PDF LOB for a book
   */
  FUNCTION get_pdf(
    p_book_id IN NUMBER
  ) RETURN BLOB;

  /**
   * Fetches the cover-image LOB for a book
   */
  FUNCTION get_cover(
    p_book_id IN NUMBER
  ) RETURN BLOB;
END book_pkg;
/
  
-- 2) Body
CREATE OR REPLACE PACKAGE BODY book_pkg AS

  PROCEDURE list_books(p_cursor OUT SYS_REFCURSOR) IS
  BEGIN
    OPEN p_cursor FOR
      SELECT book_id,
             title,
             author,
             isbn,
             category_id,
             total_copies,
             available_copies
        FROM books
       ORDER BY title;
  END list_books;


  PROCEDURE add_book(
    p_title        IN VARCHAR2,
    p_author       IN VARCHAR2,
    p_isbn         IN VARCHAR2,
    p_category_id  IN NUMBER,
    p_total_copies IN NUMBER,
    p_pdf_blob     IN BLOB,
    p_cover_blob   IN BLOB,
    p_uploaded_by  IN NUMBER,
    p_book_id      OUT NUMBER
  ) IS
  BEGIN
    INSERT INTO books(
      title, author, isbn, category_id,
      total_copies, available_copies,
      pdf_blob, cover_blob, uploaded_by
    )
    VALUES (
      p_title, p_author, p_isbn, p_category_id,
      p_total_copies, p_total_copies,
      p_pdf_blob, p_cover_blob, p_uploaded_by
    )
    RETURNING book_id INTO p_book_id;

    COMMIT;
  END add_book;


  PROCEDURE remove_book(p_book_id IN NUMBER) IS
  BEGIN
    DELETE FROM books
     WHERE book_id = p_book_id;
    COMMIT;
  END remove_book;


  FUNCTION get_pdf(p_book_id IN NUMBER) RETURN BLOB IS
    v_blob BLOB;
  BEGIN
    SELECT pdf_blob
      INTO v_blob
      FROM books
     WHERE book_id = p_book_id;
    RETURN v_blob;
  END get_pdf;


  FUNCTION get_cover(p_book_id IN NUMBER) RETURN BLOB IS
    v_blob BLOB;
  BEGIN
    SELECT cover_blob
      INTO v_blob
      FROM books
     WHERE book_id = p_book_id;
    RETURN v_blob;
  END get_cover;

END book_pkg;
/
