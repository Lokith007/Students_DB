import sqlite3
import ollama

# Connect to database
conn = sqlite3.connect("college.db")
cursor = conn.cursor()

print("Ask me (or type 'exit'):")

while True:
    question = input("\n> ").strip()
    if question.lower() == "exit":
        break

    # Send to LLM to convert to SQL
    prompt = f"""
    You are an assistant that converts natural language questions into SQLite SQL queries.
    Database schema:
    Table students(registration_no TEXT, name TEXT, batch TEXT, department TEXT, quota TEXT, cutoff REAL, cgpa REAL, projects TEXT)
    Table alumni(registration_no TEXT, name TEXT, batch TEXT, department TEXT, placed TEXT, company TEXT, role TEXT)
    Respond ONLY with the SQL query without explanation or formatting.
    Question: {question}
    """

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract content correctly from Ollama's response
        sql_query = response["message"]["content"]
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        print(f"\n[DEBUG] Generated SQL: {sql_query}\n")

        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No results found.")

        except Exception as e:
            print(f"❌ SQL Error: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")

conn.close()
