# admin.py  —  Admin panel functions
# ─────────────────────────────────────────────────────────────
# Admin PIN is hardcoded as "admin123".
# Functions: add student, view all students, mark a course completed.
# ─────────────────────────────────────────────────────────────

import oracledb
from db import get_connection
from courses import view_all_courses

ADMIN_PIN = "admin123"

def header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def verify_admin() -> bool:
    pin = input("\n  Admin PIN: ").strip()
    if pin == ADMIN_PIN:
        return True
    print("  Wrong PIN. Access denied.\n")
    return False


def add_student():
    """Insert a new student into the STUDENT table."""
    print("\n" + "─" * 50)
    print("  ADD NEW STUDENT")
    print("─" * 50)

    full_name = input("  Full Name        : ").strip()
    email     = input("  Email            : ").strip()
    password  = input("  Password         : ").strip()
    dept      = input("  Department       : ").strip()

    try:
        semester = int(input("  Current Semester : ").strip())
    except ValueError:
        semester = 1

    conn   = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO STUDENT
                (student_id, full_name, email, pass_word, department, current_semester, status)
            VALUES
                (seq_student.NEXTVAL, :name, :email, :pwd, :dept, :sem, 'active')
        """, name=full_name, email=email, pwd=password, dept=dept, sem=semester)
        conn.commit()

        # Fetch the new ID
        cursor.execute("SELECT seq_student.CURRVAL FROM DUAL")
        new_id = cursor.fetchone()[0]
        print(f"\n  Student added! New Student ID: {new_id}\n")

    except oracledb.IntegrityError as e:
        if "ORA-00001" in str(e):
            print("\n  A student with this email already exists.\n")
        else:
            print(f"\n  Error: {e}\n")
    finally:
        cursor.close()
        conn.close()


def view_all_students():
    """Display all students in the STUDENT table."""
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, full_name, email, department, current_semester, status
        FROM   STUDENT
        ORDER BY student_id
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n" + "─" * 75)
    print("  ALL STUDENTS")
    print("─" * 75)
    print(f"  {'ID':<6} {'Name':<22} {'Email':<26} {'Dept':<6} {'Sem':<5} {'Status'}")
    print("  " + "-" * 71)

    for row in rows:
        print(f"  {row[0]:<6} {row[1]:<22} {row[2]:<26} {row[3] or '':<6} {row[4] or '':<5} {row[5]}")

    print(f"\n  Total: {len(rows)} student(s)\n")

def toggle_student_status():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        header("SUSPEND / ACTIVATE STUDENT")
        sid = input("  Enter Student ID: ").strip()
        new_status = input("  Enter new status (active/suspended): ").strip().lower()
        
        if new_status not in ['active', 'suspended']:
            print("  Invalid status. Use 'active' or 'suspended'.")
            return

        cursor.execute("""
            UPDATE STUDENT 
            SET status = :status 
            WHERE student_id = :sid
        """, status=new_status, sid=sid)
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"  Success: Student {sid} is now {new_status}.")
        else:
            print("  Error: Student ID not found.")
            
    except Exception as e:
        print(f"  Database error: {e}")
    finally:
        cursor.close()
        conn.close()


def mark_course_completed():
    """
    Mark a specific course as completed for a student.
    This removes the course from their available list for future registration.
    """
    print("\n" + "─" * 50)
    print("  MARK COURSE AS COMPLETED")
    print("─" * 50)

    view_all_students()
    try:
        student_id = int(input("  Student ID  : ").strip())
    except ValueError:
        print("  Invalid input.\n"); return

    view_all_courses()
    try:
        course_id = int(input("  Course ID   : ").strip())
    except ValueError:
        print("  Invalid input.\n"); return

    grade = input("  Grade (A/B/C/D/F) : ").strip().upper()
    if grade not in ("A", "B", "C", "D", "F"):
        print("  Invalid grade. Must be A, B, C, D, or F.\n"); return

    conn   = get_connection()
    cursor = conn.cursor()

    try:
        # If they had an active enrollment, drop it first
        cursor.execute("""
            UPDATE ENROLLMENT
            SET    status = 'dropped'
            WHERE  student_id = :sid
            AND    course_id  = :cid
            AND    status     = 'active'
        """, sid=student_id, cid=course_id)

        cursor.execute("""
            INSERT INTO COMPLETED_COURSE
                (record_id, student_id, course_id, grade, completion_date)
            VALUES
                (seq_completed.NEXTVAL, :sid, :cid, :grade, SYSDATE)
        """, sid=student_id, cid=course_id, grade=grade)

        conn.commit()
        print(f"\n  Course marked as completed with grade {grade}.")
        print("  Student can no longer register for this course.\n")

    except oracledb.IntegrityError as e:
        print(f"\n  Error: {e}\n")
    finally:
        cursor.close()
        conn.close()
