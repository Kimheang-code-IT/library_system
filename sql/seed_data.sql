-- sql/seed_data.sql

-- Turn off substitution so "&" is literal
SET DEFINE OFF;

-- (Optional) start fresh on repeated runs
TRUNCATE TABLE download_logs;
TRUNCATE TABLE read_logs;
TRUNCATE TABLE fines;
TRUNCATE TABLE reservations;
TRUNCATE TABLE borrow_txns;
TRUNCATE TABLE students;
TRUNCATE TABLE books;
TRUNCATE TABLE users;
TRUNCATE TABLE categories;
TRUNCATE TABLE terms;
COMMIT;

-- 1) Admin user (we’ll hard-code the SHA1 of “adminpass”)
INSERT /*+ APPEND */ INTO users
  (username, password_hash, email, role, status, created_at)
VALUES (
  'admin',
  HEXTORAW('74913F5CD5F61EC0BCFDB775414C2FB3D161B620'),
  'admin@university.edu',
  'ADMIN',
  'ACTIVE',
  SYSDATE
);
COMMIT;

-- 2) Two sample terms
INSERT /*+ APPEND */ INTO terms(name,start_date,end_date)
VALUES ('Fall 2025',
  TO_DATE('2025-09-01','YYYY-MM-DD'),
  TO_DATE('2025-12-20','YYYY-MM-DD')
);
INSERT /*+ APPEND */ INTO terms(name,start_date,end_date)
VALUES ('Spring 2026',
  TO_DATE('2026-01-10','YYYY-MM-DD'),
  TO_DATE('2026-05-15','YYYY-MM-DD')
);
COMMIT;

-- 3) Three sample categories
INSERT /*+ APPEND */ INTO categories(name,description)
VALUES ('Science',  'Science & Technology books');
INSERT /*+ APPEND */ INTO categories(name,description)
VALUES ('Literature','Fiction & Poetry');
INSERT /*+ APPEND */ INTO categories(name,description)
VALUES ('History',  'World & Regional History');
COMMIT;

-- Restore default behavior (if you ever need it)
SET DEFINE ON;
