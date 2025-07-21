-- sql/add_student.sql
SET DEFINE OFF;

-- 1) Insert the user with SHA1("studentpass") = B98D463190B1F2E3B447D2F4A68BEE1AB29D6316
INSERT INTO users (
  username,
  password_hash,
  email,
  role,
  status,
  created_at
) VALUES (
  'student1',
  HEXTORAW('B98D463190B1F2E3B447D2F4A68BEE1AB29D6316'),
  'student1@university.edu',
  'STUDENT',
  'ACTIVE',
  SYSDATE
);
COMMIT;

-- 2) Insert the student profile, using the user_id we just created
INSERT INTO students (
  user_id,
  department,
  year
) VALUES (
  -- lookup the new user_id
  (SELECT user_id FROM users WHERE username = 'student1'),
  'Computer Science',
  1
);
COMMIT;

SET DEFINE ON;
