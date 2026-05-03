# enrollment.py  —  Register, drop, view enrollments & completed courses
# ─────────────────────────────────────────────────────────────

import oracledb
from db import get_connection
from courses import view_available


def register_course(student_id: int):
    """
    Shows available courses then lets the student pick one to register.
    Blocks registration if the course is already completed (checked via SQL).
    Blocks duplicate registration via UNIQUE constraint (ORA-00001).
    """
    rows = view_available(student_id)
    if not rows:
        return

    print("  Enter Course ID to register (0 to cancel): ", end="")
    try:
        course_id = int(input().strip())
    except ValueError:
        print("  Invalid input.")
        return

    if course_id == 0:
        return

    conn   = get_connection()
    cursor = conn.cursor()

    # ── Block if already completed ─────────────────────────────
    cursor.execute("""
        SELECT COUNT(*)
        FROM   COMPLETED_COURSE
        WHERE  student_id = :sid
        AND    course_id  = :cid
    """, sid=student_id, cid=course_id)

    already_done = cursor.fetchone()[0]

    if already_done > 0:
        # Get course name for a friendly message
        cursor.execute("SELECT course_name FROM COURSE WHERE course_id = :cid", cid=course_id)
        row = cursor.fetchone()
        name = row[0] if row else f"Course {course_id}"
        cursor.close()
        conn.close()
        print(f"\n  BLOCKED: You already completed \"{name}\".")
        print("  Re-registration of completed courses is not allowed.\n")
        return

    # ── Insert enrollment ──────────────────────────────────────
    try:
        cursor.execute("""
            INSERT INTO ENROLLMENT (enrollment_id, student_id, course_id, enrolled_at, status)
            VALUES (seq_enrollment.NEXTVAL, :sid, :cid, SYSDATE, 'active')
        """, sid=student_id, cid=course_id)
        conn.commit()

        cursor.execute("SELECT course_name FROM COURSE WHERE course_id = :cid", cid=course_id)
        row = cursor.fetchone()
        name = row[0] if row else f"Course {course_id}"

        print(f"\n  Successfully registered for \"{name}\"!\n")

    except oracledb.IntegrityError as e:
        error_msg = str(e)
        if "ORA-00001" in error_msg:
            print("\n  You are already enrolled in this course.\n")
        elif "ORA-02291" in error_msg:
            print("\n  Course ID not found.\n")
        else:
            print(f"\n  Database error: {error_msg}\n")

    finally:
        cursor.close()
        conn.close()


def drop_course(student_id: int):
    """
    Shows active enrollments, then lets the student pick one to drop.
    """
    enrollments = view_my_enrollments(student_id)
    if not enrollments:
        return

    print("  Enter Enrollment ID to drop (0 to cancel): ", end="")
    try:
        enroll_id = int(input().strip())
    except ValueError:
        print("  Invalid input.")
        return

    if enroll_id == 0:
        return

    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM ENROLLMENT 
    WHERE enrollment_id = :eid AND student_id = :sid
""", eid=enroll_id, sid=student_id)

    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()

    if affected == 1:
        print("\n  Course dropped successfully.\n")
    else:
        print("\n  Enrollment ID not found or already dropped.\n")


def view_my_enrollments(student_id: int) -> list:
    """Shows all active enrollments for the student."""
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.enrollment_id,
               c.course_name,
               c.credit_hours,
               f.faculty_name,
               e.enrolled_at,
               e.status
        FROM   ENROLLMENT e
        JOIN   COURSE  c ON e.course_id  = c.course_id
        JOIN   FACULTY f ON c.faculty_id = f.faculty_id
        WHERE  e.student_id = :sid
        AND    e.status     = 'active'
        ORDER BY e.enrollment_id
    """, sid=student_id)

    rows = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(c.credit_hours)
        FROM   ENROLLMENT e
        JOIN   COURSE c ON e.course_id = c.course_id
        WHERE  e.student_id = :sid
        AND    e.status     = 'active'
    """, sid=student_id)
    total_credits = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    print("\n" + "─" * 70)
    print("  MY CURRENT ENROLLMENTS")
    print("─" * 70)

    if not rows:
        print("  No active enrollments.\n")
        return []

    print(f"  {'Enroll ID':<10} {'Course Name':<28} {'Credits':<8} {'Faculty':<18} {'Date'}")
    print("  " + "-" * 66)

    for row in rows:
        date_str = row[4].strftime("%Y-%m-%d") if row[4] else "—"
        print(f"  {row[0]:<10} {row[1]:<28} {row[2]:<8} {row[3]:<18} {date_str}")

    print(f"\n  Total: {len(rows)} course(s)  |  {total_credits} credit hours\n")
    return rows


def view_completed_courses(student_id: int):
    """Shows all courses the student has completed (with grade)."""
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cc.record_id,
               c.course_name,
               c.credit_hours,
               f.faculty_name,
               cc.grade,
               cc.completion_date
        FROM   COMPLETED_COURSE cc
        JOIN   COURSE  c ON cc.course_id = c.course_id
        JOIN   FACULTY f ON c.faculty_id = f.faculty_id
        WHERE  cc.student_id = :sid
        ORDER BY cc.completion_date
    """, sid=student_id)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n" + "─" * 70)
    print("  MY COMPLETED COURSES")
    print("─" * 70)

    if not rows:
        print("  No completed courses on record.\n")
        return

    print(f"  {'ID':<5} {'Course Name':<28} {'Credits':<8} {'Faculty':<18} {'Grade':<6} {'Date'}")
    print("  " + "-" * 66)

    for row in rows:
        date_str = row[5].strftime("%Y-%m-%d") if row[5] else "—"
        print(f"  {row[0]:<5} {row[1]:<28} {row[2]:<8} {row[3]:<18} {row[4]:<6} {date_str}")

    print(f"\n  Total completed: {len(rows)} course(s)\n")
