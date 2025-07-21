-- sql/borrow_pkg.sql

-- 1) Package spec
CREATE OR REPLACE PACKAGE borrow_pkg AS

  /** 
   * Checks out a book for a student in a given term.
   * @param p_student_id  the STUDENTS.student_id
   * @param p_book_id     the BOOKS.book_id
   * @param p_term_id     the TERMS.term_id
   * @param p_due_days    number of days until due (default: 14)
   * @param p_txn_id OUT  the new transaction ID
   */
  PROCEDURE checkout_book(
    p_student_id IN NUMBER,
    p_book_id    IN NUMBER,
    p_term_id    IN NUMBER,
    p_due_days   IN NUMBER DEFAULT 14,
    p_txn_id     OUT NUMBER
  );

  /**
   * Returns a book by transaction ID.
   * Automatically calculates a fine of $1 per day late (if any).
   * @param p_txn_id the BORROW_TXNS.txn_id
   */
  PROCEDURE return_book(
    p_txn_id IN NUMBER
  );

  /**
   * Lists all active loans for a student.
   * @param p_student_id the STUDENTS.student_id
   * @param p_cursor  OUT SYS_REFCURSOR of (txn_id, book_id, borrow_date, due_date, status)
   */
  PROCEDURE list_borrowed(
    p_student_id IN NUMBER,
    p_cursor     OUT SYS_REFCURSOR
  );

END borrow_pkg;
/
  
-- 2) Package body
CREATE OR REPLACE PACKAGE BODY borrow_pkg AS

  PROCEDURE checkout_book(
    p_student_id IN NUMBER,
    p_book_id    IN NUMBER,
    p_term_id    IN NUMBER,
    p_due_days   IN NUMBER,
    p_txn_id     OUT NUMBER
  ) IS
    v_avail NUMBER;
  BEGIN
    -- 1) Check availability
    SELECT available_copies
      INTO v_avail
      FROM books
     WHERE book_id = p_book_id;
    IF v_avail < 1 THEN
      RAISE_APPLICATION_ERROR(-20001, 'No copies available');
    END IF;

    -- 2) Insert transaction
    INSERT INTO borrow_txns (
      student_id, book_id, term_id,
      borrow_date, due_date, status
    ) VALUES (
      p_student_id,
      p_book_id,
      p_term_id,
      SYSDATE,
      SYSDATE + p_due_days,
      'OUT'
    )
    RETURNING txn_id INTO p_txn_id;

    -- 3) Update counts
    UPDATE books
       SET available_copies = available_copies - 1
     WHERE book_id = p_book_id;

    UPDATE students
       SET borrow_count = borrow_count + 1
     WHERE student_id = p_student_id;

    COMMIT;
  END checkout_book;


  PROCEDURE return_book(
    p_txn_id IN NUMBER
  ) IS
    v_due      DATE;
    v_ret      DATE := SYSDATE;
    v_book_id  NUMBER;
    v_student  NUMBER;
    v_diff     NUMBER;
    v_fine_amt NUMBER;
  BEGIN
    -- 1) Fetch due date, book and student
    SELECT due_date, book_id, student_id
      INTO v_due, v_book_id, v_student
      FROM borrow_txns
     WHERE txn_id = p_txn_id;

    -- 2) Update transaction
    UPDATE borrow_txns
       SET return_date = v_ret,
           status      = 'RETURNED'
     WHERE txn_id = p_txn_id;

    -- 3) Update counts
    UPDATE books
       SET available_copies = available_copies + 1
     WHERE book_id = v_book_id;

    UPDATE students
       SET borrow_count = borrow_count - 1
     WHERE student_id = v_student;

    -- 4) If late, insert a $1/day fine
    v_diff := TRUNC(v_ret) - TRUNC(v_due);
    IF v_diff > 0 THEN
      INSERT INTO fines(txn_id, amount, paid_flag)
      VALUES (p_txn_id, v_diff * 1, 'N');
    END IF;

    COMMIT;
  END return_book;


  PROCEDURE list_borrowed(
    p_student_id IN NUMBER,
    p_cursor     OUT SYS_REFCURSOR
  ) IS
  BEGIN
    OPEN p_cursor FOR
      SELECT txn_id,
             book_id,
             borrow_date,
             due_date,
             return_date,
             status
        FROM borrow_txns
       WHERE student_id = p_student_id
       ORDER BY borrow_date DESC;
  END list_borrowed;

END borrow_pkg;
/
