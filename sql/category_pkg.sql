-- sql/category_pkg.sql

-- 1) Package spec
CREATE OR REPLACE PACKAGE category_pkg AS
  /** 
   * Returns all categories in a SYS_REFCURSOR
   */
  PROCEDURE list_categories(
    p_cursor OUT SYS_REFCURSOR
  );

  /**
   * Adds a new category
   */
  PROCEDURE add_category(
    p_name        IN VARCHAR2,
    p_description IN VARCHAR2
  );

  /**
   * Updates an existing category
   */
  PROCEDURE edit_category(
    p_id          IN NUMBER,
    p_name        IN VARCHAR2,
    p_description IN VARCHAR2
  );

  /**
   * Deletes a category by ID
   */
  PROCEDURE remove_category(
    p_id IN NUMBER
  );
END category_pkg;
/
  
-- 2) Package body
CREATE OR REPLACE PACKAGE BODY category_pkg AS

  PROCEDURE list_categories(
    p_cursor OUT SYS_REFCURSOR
  ) IS
  BEGIN
    OPEN p_cursor FOR
      SELECT category_id, name, description
        FROM categories
       ORDER BY name;
  END list_categories;

  PROCEDURE add_category(
    p_name        IN VARCHAR2,
    p_description IN VARCHAR2
  ) IS
  BEGIN
    INSERT INTO categories(name, description)
    VALUES (p_name, p_description);
    COMMIT;
  END add_category;

  PROCEDURE edit_category(
    p_id          IN NUMBER,
    p_name        IN VARCHAR2,
    p_description IN VARCHAR2
  ) IS
  BEGIN
    UPDATE categories
       SET name        = p_name,
           description = p_description
     WHERE category_id = p_id;
    COMMIT;
  END edit_category;

  PROCEDURE remove_category(
    p_id IN NUMBER
  ) IS
  BEGIN
    DELETE FROM categories
     WHERE category_id = p_id;
    COMMIT;
  END remove_category;

END category_pkg;
/
