# courses.py  —  View available courses
# ─────────────────────────────────────────────────────────────
# Queries COURSE joined with FACULTY.
# Automatically excludes courses the student already completed
# and courses they are currently enrolled in.
# ─────────────────────────────────────────────────────────────

from db import get_connection


def view_available(student_id: int) -> list:
    """
    Prints available courses for the student and returns them as a list.
    Completed courses and active enrollments are filtered out via SQL.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.course_id,
               c.course_name,
               c.credit_hours,
               f.faculty_name,
               c.semester,
               c.year_val,
               c.max_seats
        FROM   COURSE  c
        JOIN   FACULTY f ON c.faculty_id = f.faculty_id
        WHERE  c.course_id NOT IN (
                   SELECT course_id
                   FROM   COMPLETED_COURSE
                   WHERE  student_id = :sid
               )
        AND    c.course_id NOT IN (
                   SELECT course_id
                   FROM   ENROLLMENT
                   WHERE  student_id = :sid
                   AND    status     = 'active'
               )
        ORDER BY c.course_id
    """, sid=student_id)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n" + "─" * 70)
    print("  AVAILABLE COURSES")
    print("─" * 70)

    if not rows:
        print("  No courses available for registration.")
        return []

    print(f"  {'ID':<5} {'Course Name':<28} {'Credits':<8} {'Faculty':<18} {'Semester'}")
    print("  " + "-" * 66)

    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<28} {row[2]:<8} {row[3]:<18} {row[4]} {row[5]}")

    print(f"\n  [Completed courses are automatically hidden from this list]\n")
    return rows


def view_all_courses() -> list:
    """Admin view — shows every course with faculty info."""
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.course_id, c.course_name, c.credit_hours,
               f.faculty_name, c.semester, c.year_val, c.max_seats
        FROM   COURSE  c
        JOIN   FACULTY f ON c.faculty_id = f.faculty_id
        ORDER BY c.course_id
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n" + "─" * 70)
    print("  ALL COURSES")
    print("─" * 70)
    print(f"  {'ID':<5} {'Course Name':<28} {'Credits':<8} {'Faculty':<18} {'Semester'}")
    print("  " + "-" * 66)

    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<28} {row[2]:<8} {row[3]:<18} {row[4]} {row[5]}")

    return rows
