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
    Table students(
        email TEXT,
        reg_no TEXT PRIMARY KEY,
        name TEXT,
        section TEXT,
        gender TEXT,
        accommodation TEXT,
        quota TEXT,
        state TEXT,
        medium TEXT,
        first_graduate TEXT,
        pmss_scholarship TEXT,
        college_tshirt_size TEXT,
        community TEXT,
        sub_caste_name TEXT,
        address_for_communication TEXT,
        student_phone_1 TEXT,
        student_phone_2 TEXT,
        father_contact_number TEXT,
        mother_contact_number TEXT,
        guardian_contact_number TEXT,
        personal_mail_id TEXT,
        official_mail_id TEXT,
        date_of_birth TEXT,
        father_name_with_initial TEXT,
        mother_name_with_initial TEXT,
        father_occupation TEXT,
        father_designation TEXT,
        father_working_company_name TEXT,
        mother_occupation TEXT,
        mother_designation TEXT,
        mother_working_company_name TEXT,
        xth_standard_total_marks REAL,
        xth_board TEXT,
        xiith_standard_total_marks REAL,
        xiith_standard_cutoff_pcm REAL,
        xiith_board TEXT,
        semester_1_gpa REAL,
        semester_1_arrears_count INTEGER,
        semester_1_arrear_subjects TEXT,
        arrear_subject_title TEXT
    )
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
