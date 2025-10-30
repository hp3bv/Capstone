import sqlite3
import os

# Point to your database file
db_path = os.path.abspath("group_management.db")
print(f"Connecting to database at: {db_path}")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the 'users' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
if not cursor.fetchone():
    print("❌ The 'user' table does not exist in this database.")
else:
    print("✅ 'user' table found.\n")

    # Print all usernames
    cursor.execute("SELECT username, email, role_id, created_at FROM user;")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No users found in the 'user' table.")
    else:
        print("📋 Users in database:")
        for row in rows:
            print(f" - Username: {row[0]}, Email: {row[1]}, Role ID: {row[2]}, Created: {row[3]}")

# Close connection
conn.close()
