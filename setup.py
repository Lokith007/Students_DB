import sqlite3

# Connect to SQLite DB (will create file if not exists)
conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# Create alumni table
cursor.execute("""
CREATE TABLE IF NOT EXISTS alumni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    batch INTEGER,
    department TEXT,
    company TEXT,
    role TEXT
)
""")

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year INTEGER,
    department TEXT,
    email TEXT
)
""")

# Insert sample alumni data
cursor.executemany("""
INSERT INTO alumni (name, batch, department, company, role)
VALUES (?, ?, ?, ?, ?)
""", [
    ("Alice Johnson", 2020, "CSE", "Google", "Software Engineer"),
    ("Bob Kumar", 2019, "ECE", "Microsoft", "Data Analyst"),
    ("Priya Sharma", 2021, "CSE", "Amazon", "ML Engineer")
])

# Insert sample students data
cursor.executemany("""
INSERT INTO students (name, year, department, email)
VALUES (?, ?, ?, ?)
""", [
    ("Rahul Mehta", 3, "CSE", "rahul@college.edu"),
    ("Neha Singh", 2, "EEE", "neha@college.edu")
])

# Save and close
conn.commit()
conn.close()

print("✅ Database setup complete! college.db created.")
