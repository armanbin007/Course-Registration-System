# auth.py  —  Student login / logout
# ─────────────────────────────────────────────────────────────

from db import get_connection


def login() -> dict | None:
    """
    Prompts for student ID and password.
    Returns student dict if credentials match, None otherwise.
    """
    print("\n" + "─" * 50)
    print("  STUDENT LOGIN")
    print("─" * 50)

    try:
        student_id = int(input("  Student ID : ").strip())
    except ValueError:
        print("  Invalid ID. Must be a number.")
        return None

    password = input("  Password   : ").strip()

    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, full_name, email, department, current_semester, status
        FROM   STUDENT
        WHERE  student_id = :sid
        AND    pass_word  = :pwd
        AND    status     = 'active'
    """, sid=student_id, pwd=password)

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        student = {
            "id":         row[0],
            "name":       row[1],
            "email":      row[2],
            "department": row[3],
            "semester":   row[4],
            "status":     row[5],
        }
        print(f"\n  Login successful! Welcome, {student['name']}.")
        return student

    print("\n  Invalid Student ID or password. Please try again.")
    return None
