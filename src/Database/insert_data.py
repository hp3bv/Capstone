import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Insert initial data into the database.")
parser.add_argument("-d", "--db", required=True, help="Path to SQLite database")
args = parser.parse_args()

conn = sqlite3.connect(args.db)
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO role (role_name) VALUES ('student');")
cursor.execute("INSERT OR IGNORE INTO role (role_name) VALUES ('group_org');")
cursor.execute("INSERT OR IGNORE INTO role (role_name) VALUES ('admin');")

cursor.execute("INSERT OR IGNORE INTO study_group (group_name) VALUES ('ROOT');")

conn.commit()
conn.close()

print("Data initialized!")