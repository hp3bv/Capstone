import pytest
import sqlite3
from src.Server.invokers.db.db_invoker import DBInvoker

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS university (
    university_id INTEGER PRIMARY KEY AUTOINCREMENT,
    university_name TEXT
);

CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attends_university INTEGER,
    FOREIGN KEY (attends_university) REFERENCES university(university_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    course_code TEXT,
    course_subject TEXT,
    course_university_id INTEGER,
    FOREIGN KEY (course_university_id) REFERENCES university(university_id) ON DELETE CASCADE,
    UNIQUE (course_code, course_subject, course_university_id)
);

CREATE TABLE IF NOT EXISTS study_group (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    course_id INTEGER,
    organizer_username TEXT,
    max_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (organizer_username) REFERENCES user(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS membership (
    username TEXT,
    group_id INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT 1,
    role_id INTEGER,
    PRIMARY KEY (username, group_id),
    FOREIGN KEY (username) REFERENCES user(username) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE SET NULL,
    FOREIGN KEY (group_id) REFERENCES study_group(group_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    username TEXT,
    content TEXT,
    message_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES study_group(group_id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES user(username) ON DELETE CASCADE
);
"""

@pytest.fixture
def db_invoker():
    invoker = DBInvoker(":memory:")
    
    try:
        invoker.cursor.executescript(SCHEMA)
        invoker.conn.commit()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Schema creation failed: {e}")
    
    yield invoker
    
    invoker.conn.close()

def test_addUser_and_getUser(db_invoker):
    db_invoker.cursor.execute("INSERT INTO role (role_id, role_name) VALUES (1, 'Student')")
    db_invoker.conn.commit()

    db_invoker.addUser("testUser", "test@test.com", "hash123")
    
    user = db_invoker.getUserFromUsername("testUser")
    assert user is not None
    assert user["email"] == "test@test.com"
    
    user_by_email = db_invoker.getUserFromEmail("test@test.com")
    assert user_by_email is not None
    assert user_by_email["username"] == "testUser"

def test_getUser_notFound(db_invoker):
    user = db_invoker.getUserFromUsername("ghost")
    assert user is None

def test_addMessage_and_getMessages(db_invoker):
    db_invoker.cursor.execute("INSERT INTO role (role_id, role_name) VALUES (1, 'Student')")
    db_invoker.addUser("chatUser", "chat@test.com", "hash")
    
    db_invoker.cursor.execute("INSERT INTO university (university_id, university_name) VALUES (1, 'Test Uni')")
    db_invoker.cursor.execute("INSERT INTO course (course_id, course_university_id) VALUES (10, 1)")
    db_invoker.cursor.execute("INSERT INTO study_group (group_id, course_id, organizer_username) VALUES (1, 10, 'chatUser')")
    db_invoker.conn.commit()

    msg_id = db_invoker.addMessage("chatUser", "Hello World", group_id=1)
    assert msg_id is not None
    
    messages = db_invoker.getMessages(1)
    
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello World"
    assert messages[0]["username"] == "chatUser"


def test_getUniversities(db_invoker):
    db_invoker.cursor.execute("INSERT INTO university (university_id, university_name) VALUES (1, 'Mizzou')")
    db_invoker.conn.commit()
    
    unis = db_invoker.getUniversities()
    assert len(unis) == 1
    if "university_name" in unis[0].keys():
        assert unis[0]["university_name"] == "Mizzou"
    else:
        assert unis[0]["name"] == "Mizzou"

def test_attends(db_invoker):
    db_invoker.cursor.execute("INSERT INTO role (role_id, role_name) VALUES (1, 'Student')")
    db_invoker.addUser("student", "s@test.com", "hash")
    db_invoker.cursor.execute("INSERT INTO university (university_id, university_name) VALUES (5, 'Mizzou')")
    db_invoker.conn.commit()
    
    db_invoker.attends("student", 5)
    
    user = db_invoker.getUserFromUsername("student")
    assert user["attends_university"] == 5

def test_courseLookup(db_invoker):
    db_invoker.cursor.execute("INSERT INTO university (university_id, university_name) VALUES (1, 'Test Uni')")
    db_invoker.cursor.execute(
        "INSERT INTO course (course_university_id, course_subject, course_code, course_name) VALUES (1, 'CS', '101', 'Intro')"
    )
    db_invoker.conn.commit()
    
    courses = db_invoker.courseLookup(1, 'CS', '101', 'Intro')
    assert len(courses) == 1
    
    assert courses[0]["courseSubj"] == "CS"
    assert courses[0]["courseCode"] == "101"

def test_group_workflow(db_invoker):
    db_invoker.cursor.execute("INSERT INTO role (role_id, role_name) VALUES (1, 'Student')")
    db_invoker.addUser("joiner", "j@test.com", "hash")
    db_invoker.cursor.execute("INSERT INTO university (university_id, university_name) VALUES (1, 'Test Uni')")
    db_invoker.cursor.execute("INSERT INTO course (course_id, course_university_id) VALUES (500, 1)")
    
    db_invoker.cursor.execute(
        "INSERT INTO study_group (group_id, course_id, max_size, organizer_username) VALUES (99, 500, 5, 'joiner')"
    )
    db_invoker.conn.commit()
    
    groups = db_invoker.getGroupsForCourse(500)
    assert len(groups) == 1
    assert groups[0]["group_id"] == 99
    
    group_detail = db_invoker.getGroup(99)
    assert group_detail is not None
    assert group_detail["group_id"] == 99
    
    try:
        db_invoker.joinGroup(99, "joiner")
    except sqlite3.OperationalError as e:
        pytest.fail(f"SQL Error in JOIN_GROUP: {e}")

    db_invoker.cursor.execute("SELECT * FROM membership WHERE username = 'joiner' AND group_id = 99")
    member_record = db_invoker.cursor.fetchone()
    assert member_record is not None
    assert member_record["username"] == "joiner"