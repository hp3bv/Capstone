import sqlite3

# Connect to the SQLite database file (will create it if it doesn't exist)
conn = sqlite3.connect('group_management.db')
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# ROLE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE
);
""")

# USER TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    role_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES role(role_id)
);
""")

# COURSE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    course_code INTEGER UNIQUE
);
""")

# STUDY GROUP TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_group (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    course_id INTEGER,
    organizer_username TEXT,
    max_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (organizer_username) REFERENCES user(username)
);
""")

# MEMBERSHIP TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS membership (
    username TEXT,
    group_id INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT 1,
    PRIMARY KEY (username, group_id),
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (group_id) REFERENCES study_group(group_id)
);
""")

# MESSAGE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    username TEXT,
    content TEXT,
    message_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES study_group(group_id),
    FOREIGN KEY (username) REFERENCES user(username)
);
""")

# ANNOUNCEMENT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS announcement (
    announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    content TEXT,
    announcement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES study_group(group_id)
);
""")

# REPORT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS report (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporter_username TEXT,
    reported_username TEXT,
    description TEXT,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reporter_username) REFERENCES user(username),
    FOREIGN KEY (reported_username) REFERENCES user(username)
);
""")

# AUDIT LOG TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    target_id INTEGER,
    audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES user(username)
);
""")

# NOTIFICATION TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("SQLite database and tables created successfully!")
