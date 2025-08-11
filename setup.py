import sqlite3

# Connect to SQLite DB
conn=sqlite3.connect("college.db")
cursor=conn.cursor()

# Drop old tables to avoid duplicates
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS alumni")

# Create fresh students table
cursor.execute("""
CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT UNIQUE,
    name TEXT,
    batch TEXT,
    department TEXT,
    quota TEXT,
    cutoff REAL,
    cgpa REAL,
    projects_completed TEXT
)
""")

# Create fresh alumni table (with placed column)
cursor.execute("""
CREATE TABLE alumni(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_no TEXT UNIQUE,
    name TEXT,
    batch TEXT,
    department TEXT,
    placed TEXT,
    company TEXT,
    role TEXT
)
""")

# Load students from file
with open("students.txt","r",encoding="utf-8") as f:
    for line in f:
        data=line.strip().split(",")
        if len(data)==8:
            cursor.execute("""
            INSERT OR IGNORE INTO students
            (roll_number,name,batch,department,quota,cutoff,cgpa,projects_completed)
            VALUES (?,?,?,?,?,?,?,?)
            """, data)

# Load alumni from file
with open("alumni.txt","r",encoding="utf-8") as f:
    for line in f:
        data=line.strip().split(",")
        if len(data)==7:
            cursor.execute("""
            INSERT OR IGNORE INTO alumni
            (registration_no,name,batch,department,placed,company,role)
            VALUES (?,?,?,?,?,?,?)
            """, data)

conn.commit()
conn.close()

print("✅ Database setup complete! Data loaded without duplicates.")
