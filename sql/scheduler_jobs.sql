-- sql/scheduler_jobs.sql

BEGIN
  -- Reset all students’ borrow_count on each term’s start_date
  FOR rec IN (SELECT term_id, start_date FROM terms) LOOP
    DBMS_SCHEDULER.CREATE_JOB (
      job_name        => 'RESET_COUNT_' || rec.term_id,
      job_type        => 'PLSQL_BLOCK',
      job_action      => 'BEGIN UPDATE students SET borrow_count = 0; END;',
      start_date      => rec.start_date,
      repeat_interval => 'FREQ=YEARLY',  -- adjust if terms span different months
      enabled         => TRUE
    );
  END LOOP;
  
  -- Daily job to send overdue notices
  DBMS_SCHEDULER.CREATE_JOB (
    job_name        => 'NOTIFY_OVERDUE',
    job_type        => 'PLSQL_BLOCK',
    job_action      => q'[
      DECLARE
        CURSOR c IS
          SELECT s.user_id, b.book_id, tx.txn_id
          FROM borrow_txns tx
          JOIN students s ON tx.student_id = s.student_id
          JOIN users u    ON s.user_id = u.user_id
          JOIN books b    ON tx.book_id    = b.book_id
          WHERE tx.status = 'OUT'
            AND tx.due_date < SYSDATE;
      BEGIN
        FOR r IN c LOOP
          -- You could call UTL_MAIL or write to a notifications table
          INSERT INTO audit_logs (user_id, action, object_type, object_id)
          VALUES (r.user_id, 'OVERDUE NOTICE', 'TXN', r.txn_id);
        END LOOP;
      END;]'
    ,
    start_date      => SYSTIMESTAMP,
    repeat_interval => 'FREQ=DAILY;BYHOUR=2;BYMINUTE=0;BYSECOND=0',
    enabled         => TRUE
  );
END;
/
COMMIT;
