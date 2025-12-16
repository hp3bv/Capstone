class Queries:
    SELECT_USERNAME = "SELECT * FROM user WHERE username = :username"
    SELECT_EMAIL = "SELECT * FROM user WHERE email = :email"
    ADD_USER = """
        INSERT INTO user (username, email, password_hash) 
        VALUES (:username, :email, :password_hash)
    """
    ADD_MESSAGE = """
        INSERT INTO message (group_id, username, content)
        VALUES (:group_id, :username, :content)
    """
    GET_MESSAGES = """
        SELECT * FROM message
        WHERE group_id = :group_id
        ORDER BY message_date ASC
        LIMIT 50
    """
    
    GET_UNIVERSITIES = """
        SELECT * 
        FROM university
        ORDER BY university_name DESC
    """
    
    ATTENDS_UNIVERSITY = """
        UPDATE user 
        SET attends_university = :uid 
        WHERE username = :username
    """
    
    COURSE_LOOKUP = """
        SELECT
            course_id AS courseId,
            course_name AS courseName,
            course_code AS courseCode,
            course_subject AS courseSubj
        FROM
            course
        WHERE
            course_university_id = :uid
            AND (:courseSubj IS NULL OR course_subject LIKE '%' || :courseSubj || '%')
            AND (:courseNo IS NULL OR course_code LIKE '%' || :courseNo || '%')
            AND (:courseName IS NULL OR course_name LIKE '%' || :courseName || '%')
    """
    
    GET_GROUPS = """
        SELECT 
            g.*,
            COUNT(m.username) AS total_users
        FROM study_group g
        LEFT JOIN membership m
            ON g.group_id = m.group_id
        WHERE g.course_id = :cid 
        GROUP BY g.group_id
        HAVING COUNT(m.username) < g.max_size
        ORDER BY total_users
    """
    
    GET_GROUP = """
        SELECT 
            g.*,
            COUNT(m.username) AS total_users
        FROM study_group g
        LEFT JOIN membership m
            ON g.group_id = m.group_id
        WHERE g.group_id = :gid 
    """
    
    JOIN_GROUP =  """
        INSERT INTO membership(username, group_id, role_id)
        VALUES (:username, :gid, 1)
    """
    
    GET_GROUPS_FOR_USER = """
        SELECT G.*
        FROM study_group G
        JOIN membership M ON G.group_id = M.group_id
        WHERE M.username = :username
    """