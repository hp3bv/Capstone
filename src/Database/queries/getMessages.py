import sqlite3
import os

# Point to your database file
db_path = os.path.abspath("group_management.db")
print(f"Connecting to database at: {db_path}")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the 'message' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message';")
if not cursor.fetchone():
    print("❌ The 'message' table does not exist in this database.")
else:
    print("✅ 'message' table found.\n")

    # Print all usernames
    cursor.execute("SELECT message_id, username, content, message_date FROM message;")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No messages found in the 'message' table.")
    else:
        print("📋 Users in database:")
        for row in rows:
            print(f" - Message ID: {row[0]}, username: {row[1]}, Content: {row[2]}, Sent on: {row[3]}")

# Close connection
conn.close()
