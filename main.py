#!/usr/bin/env python3
# main.py  —  Course Registration System
# ─────────────────────────────────────────────────────────────
# Entry point. Handles main menu, student menu, admin menu.
# Run:  python main.py
# ─────────────────────────────────────────────────────────────

import sys
from db import test_connection
from auth import login
from enrollment import (
    register_course,
    drop_course,
    view_my_enrollments,
    view_completed_courses,
)
from courses import view_available
from admin import verify_admin, add_student, view_all_students, mark_course_completed, toggle_student_status


# ─── Helpers ─────────────────────────────────────────────────

def header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def pause():
    input("\n  Press Enter to continue...")


# ─── Student menu ─────────────────────────────────────────────

def student_menu(student: dict):
    while True:
        header(f"STUDENT MENU  —  {student['name']}  (ID: {student['id']})")
        print("  1. View available courses")
        print("  2. Register for a course")
        print("  3. View my enrollments")
        print("  4. Drop a course")
        print("  5. View completed courses")
        print("  0. Logout")
        print()
        choice = input("  Choice: ").strip()

        if choice == "1":
            view_available(student["id"])
            pause()
        elif choice == "2":
            register_course(student["id"])
            pause()
        elif choice == "3":
            view_my_enrollments(student["id"])
            pause()
        elif choice == "4":
            drop_course(student["id"])
            pause()
        elif choice == "5":
            view_completed_courses(student["id"])
            pause()
        elif choice == "0":
            print(f"\n  Logged out. Goodbye, {student['name']}!\n")
            break
        else:
            print("\n  Invalid choice. Try again.")


# ─── Admin menu ───────────────────────────────────────────────

def admin_menu():
    if not verify_admin():
        return

    while True:
        header("ADMIN PANEL")
        print("  1. Add new student")
        print("  2. View all students")
        print("  3. Mark a course as completed for a student")
        print("  4. Change student status")
        print("  0. Back to main menu")
        print()
        choice = input("  Choice: ").strip()

        if choice == "1":
            add_student()
            pause()
        elif choice == "2":
            view_all_students()
            pause()
        elif choice == "3":
            mark_course_completed()
            pause()
        elif choice == '4':
            toggle_student_status()
            pause()
        elif choice == "0":
            break
        else:
            print("\n  Invalid choice. Try again.")


# ─── Main menu ────────────────────────────────────────────────

def main():
    header("COURSE REGISTRATION SYSTEM")
    print("  Connecting to Oracle...")

    try:
        ok = test_connection()
        if ok:
            print("  Oracle connected successfully.\n")
        else:
            print("  Connection test failed. Check your .env settings.\n")
            sys.exit(1)
    except SystemExit:
        sys.exit(1)

    while True:
        header("MAIN MENU")
        print("  1. Student Login")
        print("  2. Admin Panel")
        print("  0. Exit")
        print()
        choice = input("  Choice: ").strip()

        if choice == "1":
            student = login()
            if student:
                student_menu(student)
        elif choice == "2":
            admin_menu()
        elif choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)
        else:
            print("\n  Invalid choice. Try again.")


if __name__ == "__main__":
    main()
