class Queries:
    SELECT_USERNAME = "SELECT * FROM user WHERE username = :username"
    SELECT_EMAIL = "SELECT * FROM user WHERE email = :email"
    ADD_USER = """
        INSERT INTO user (username, email, password_hash, role_id)
        VALUES (:username, :email, :password_hash, :role_id)
    """
    ADD_MESSAGE = """
        INSERT INTO message (group_id, username, content)
        VALUES (:group_id, :username, :content)
    """