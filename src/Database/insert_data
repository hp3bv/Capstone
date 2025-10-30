import sqlite3

conn = sqlite3.connect("group_management.db")
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO role (role_name) VALUES ('student');")
cursor.execute("INSERT OR IGNORE INTO role (role_name) VALUES ('group_org');")
cursor.execute("INSERT OR IGNORE INTO role (role_name) VALUES ('admin');")

cursor.execute("INSERT OR IGNORE INTO study_group (group_name) VALUES ('ROOT');")

conn.commit()
conn.close()

print("Data initialized!")