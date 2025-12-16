import sqlite3
import os
import argparse

db_path = os.getenv("DB_PATH")

parser = argparse.ArgumentParser(description="Create SQLite database schema.")
parser.add_argument("-o", "--output", default=db_path, help="Path to output database")
args = parser.parse_args()

os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

conn = sqlite3.connect(args.output)
cursor = conn.cursor()

cursor.execute("""
    DROP TABLE IF EXISTS notification;
""")

cursor.execute("""
    DROP TABLE IF EXISTS audit_log;
""")

cursor.execute("""
    DROP TABLE IF EXISTS report;
""")

cursor.execute("""
    DROP TABLE IF EXISTS announcement;
""")

cursor.execute("""
    DROP TABLE IF EXISTS message;
""")

cursor.execute("""
    DROP TABLE IF EXISTS membership;
""")

cursor.execute("""
    DROP TABLE IF EXISTS study_group;
""")

cursor.execute("""
    DROP TABLE IF EXISTS course;
""")

cursor.execute("""
    DROP TABLE IF EXISTS user;
""")

cursor.execute("""
    DROP TABLE IF EXISTS university;
""")

cursor.execute("""
    DROP TABLE IF EXISTS role;
""")

conn.commit()
conn.close()

print("ALL TABLES DROPPED")