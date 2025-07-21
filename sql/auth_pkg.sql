-- sql/auth_pkg.sql

-- 1) Package specification
CREATE OR REPLACE PACKAGE auth_pkg AS
  /**
   * Validate a user by username + raw SHA1 hash.
   * @param p_username the login name
   * @param p_pw_hash  the RAW SHA1(password)
   * @return USER_ID if valid; NULL otherwise
   */
  FUNCTION login_user(
    p_username IN VARCHAR2,
    p_pw_hash   IN RAW
  ) RETURN NUMBER;
END auth_pkg;
/
  
-- 2) Package body
CREATE OR REPLACE PACKAGE BODY auth_pkg AS

  FUNCTION login_user(
    p_username IN VARCHAR2,
    p_pw_hash   IN RAW
  ) RETURN NUMBER
  IS
    v_user_id     users.user_id%TYPE;
    v_stored_hash RAW(32767);
    v_len         PLS_INTEGER := LENGTH(p_pw_hash);
  BEGIN
    -- Fetch the stored hash (first v_len bytes) as a RAW
    SELECT user_id,
           DBMS_LOB.SUBSTR(password_hash, v_len, 1)
      INTO v_user_id, v_stored_hash
      FROM users
     WHERE username = p_username;

    -- Compare in PL/SQL
    IF v_stored_hash = p_pw_hash THEN
      RETURN v_user_id;
    ELSE
      RETURN NULL;
    END IF;

  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      RETURN NULL;  -- username not found
  END login_user;

END auth_pkg;
/
