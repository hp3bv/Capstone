import sqlite3
import os
import bcrypt  # Make sure you have this installed: pip install bcrypt

def hash_password(plain_password):
    # Convert string to bytes, hash it, then decode back to string for storage
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_test_data():
    DB_PATH = os.getenv("DB_PATH")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("🌱 Seeding database with test data...")

    try:
        # ... (Roles and University creation code stays the same) ...
        # 1. Create Roles
        print("   - Creating Roles...")
        roles = [('Student',), ('Tutor',), ('Admin',)]
        cursor.executemany("INSERT OR IGNORE INTO role (role_name) VALUES (?)", roles)

        # 2. Create University
        print("   - Creating University...")
        cursor.execute("INSERT INTO university (university_name) VALUES (?)", ('University of Missouri',))
        uni_id = cursor.lastrowid

        # --- THIS IS THE FIXED SECTION ---
        # 3. Create Users
        print("   - Creating Users...")
        
        # We will set everyone's password to 'password123' for simplicity
        common_password_hash = hash_password('password123')

        users = [
            ('testUser', 'test@umsystem.edu', common_password_hash, uni_id),
            ('studyBuddy', 'buddy@umsystem.edu', common_password_hash, uni_id),
            ('groupLeader', 'leader@umsystem.edu', common_password_hash, uni_id)
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO user (username, email, password_hash, attends_university) 
            VALUES (?, ?, ?, ?)
        """, users)
        # ---------------------------------

        # ... (The rest of your script: Course, Group, Membership, Messages stays the same) ...
        
        # 4. Create Course
        print("   - Creating Course...")
        cursor.execute("""
            INSERT INTO course (course_name, course_code, course_subject, course_university_id) 
            VALUES (?, ?, ?, ?)
        """, ('Software Engineering', '4090', 'CS', uni_id))
        course_id = cursor.lastrowid

        # 5. Create Study Groups
        print("   - Creating Study Groups...")
        cursor.execute("""
            INSERT INTO study_group (group_name, course_id, organizer_username, max_size) 
            VALUES (?, ?, ?, ?)
        """, ('Capstone Survivors', course_id, 'groupLeader', 5))
        group_id1 = cursor.lastrowid

        cursor.execute("""
            INSERT INTO study_group (group_name, course_id, organizer_username, max_size) 
            VALUES (?, ?, ?, ?)
        """, ('Capstone Comrades', course_id, 'groupLeader', 5))
        group_id2 = cursor.lastrowid


        # 6. Create Memberships
        print("   - Adding Memberships...")
        memberships = [
            ('groupLeader', group_id1, 1),
            ('testUser', group_id1, 1),
            ('studyBuddy', group_id1, 1),
            ('groupLeader', group_id2, 1),
            ('testUser', group_id2, 1),
            ('studyBuddy', group_id2, 1)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO membership (username, group_id, role_id) 
            VALUES (?, ?, ?)
        """, memberships)

        # 7. Create Messages
        print("   - Creating Messages...")
        messages = [
            (group_id1, 'groupLeader', 'Welcome to the capstone group everyone!'),
            (group_id1, 'testUser', 'Hey! Thanks for adding me.'),
            (group_id1, 'studyBuddy', 'Does anyone know when the next deliverable is due?'),
            (group_id1, 'testUser', 'I think it is next Friday.'),
            (group_id1, 'groupLeader', 'Correct. Let\'s meet up this weekend to work on it.'),
            (group_id2, 'groupLeader', 'Hey guys, this is my other group!'),
        ]
        cursor.executemany("""
            INSERT INTO message (group_id, username, content) 
            VALUES (?, ?, ?)
        """, messages)

        conn.commit()
        print(f"✅ Successfully seeded data! Group ID: {group_id1} & {group_id2}")
        print("🔑 Login with Username: 'testUser' and Password: 'password123'")

    except sqlite3.IntegrityError as e:
        print(f"⚠️  Integrity Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_test_data()