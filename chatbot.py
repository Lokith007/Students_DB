import sqlite3
import subprocess

DB_PATH = "college.db"

def ask_ollama(prompt):
    """Send a prompt to Ollama and return its output (UTF-8 safe)."""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True, text=True, encoding="utf-8", errors="ignore"
    )
    return result.stdout.strip()


def query_database(sql):
    """Run SQL query on SQLite DB and return results."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return f"SQL Error: {e}"

while True:
    user_input = input("\nAsk me (or type 'exit'): ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Step 1: Convert question to SQL
    ollama_prompt = f"""
    You are an assistant that converts English questions into valid SQL queries
    for a SQLite database with these tables:
    alumni(name, batch, department, company, role)
    students(name, year, department, email)
    Return ONLY the SQL query without explanations.
    Question: {user_input}
    """

    sql_query = ask_ollama(ollama_prompt)
    print(f"\n[DEBUG] Generated SQL: {sql_query}")

    # Step 2: Run SQL on database
    results = query_database(sql_query)

    # Step 3: If results found, format nicely
    if isinstance(results, list) and results:
        formatted = "\n".join([", ".join(map(str, row)) for row in results])
        print("\n📌 Answer:\n" + formatted)
    elif isinstance(results, list) and not results:
        print("\n⚠ No results found.")
    else:
        print(f"\n❌ Error: {results}")
