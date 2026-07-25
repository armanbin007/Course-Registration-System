<p align="center">
  <img src="assets/hero.svg" alt="Course Registration System" width="100%"/>
</p>

<h1 align="center">Course Registration System</h1>
<p align="center">
  A console-based Python application backed by an Oracle 21c relational database, built to manage student course registration for a university — securely, with permanent storage and real business rules.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/language-Python-3776AB" alt="Python"/>
  <img src="https://img.shields.io/badge/database-Oracle%2021c-B91C1C" alt="Oracle 21c"/>
  <img src="https://img.shields.io/badge/driver-oracledb-0d9488" alt="oracledb"/>
  <img src="https://img.shields.io/badge/status-completed-brightgreen" alt="Status"/>
</p>

---

## Overview

A basic registration system just stores enrollments in memory and forgets everything on exit — with no way to stop a student re-registering for a course they already passed. This project fixes both problems. Every action is backed by a real Oracle database, and completed courses are permanently blocked from re-registration at both the application and database level.

## Features

| Feature | Description |
|---|---|
| 🔐 Secure login | Students authenticate with Student ID and password before accessing any course data |
| 📚 Smart course listing | Automatically hides courses the student has already completed or is currently enrolled in |
| 🚫 Completion blocking | A dedicated `COMPLETED_COURSE` table is checked before every enrollment — no re-registering a passed course |
| ➕ Enrollment & drop | Register for or drop a course, with ownership checks so students can only modify their own enrollments |
| 🛠️ Admin panel | Add new students, view all registrations, and mark courses as completed |
| 💾 Permanent storage | Every insert/update is committed to Oracle 21c across five relational tables — nothing is lost between sessions |

## Database design

Five tables connected through primary and foreign keys enforce referential integrity:

- **`STUDENT`** — student_id (PK), full_name, password, department, current_semester, status, email
- **`FACULTY`** — faculty_id (PK), faculty_name, department, email
- **`COURSE`** — course_id (PK), course_name, credit_hours, faculty_id (FK), max_seat, semester, year
- **`ENROLLMENT`** — enrollment_id (PK), student_id (FK), course_id (FK), enrolled_at, status
- **`COMPLETED_COURSE`** — record_id (PK), student_id (FK), course_id (FK), completion_date, grade

Oracle sequences (`seq_student`, `seq_course`, etc.) auto-generate primary keys, and `CHECK` / `UNIQUE` / `NOT NULL` / `REFERENCES` constraints enforce business rules directly at the database level — independent of the application code.

## How it's built

The codebase is split by concern, each in its own module:

- **`db.py`** — a single `get_connection()` function, reused across every module to avoid duplicated connection logic
- **`auth.py`** — student login and credential verification
- **`courses.py`** — course listing with automatic filtering (completed + already-enrolled courses hidden)
- **`enrollment.py`** — registration and drop logic, including the completion-block check
- **`admin.py`** — admin operations: adding students, marking course completions
- **`main.py`** — the console menu and overall navigation

All SQL queries use Oracle bind variables (`:sid`, `:cid`) to prevent SQL injection and improve query performance, and every write is followed by `conn.commit()` to persist it permanently.

## Example output

```
============================================================
 COURSE REGISTRATION SYSTEM
============================================================
 Connecting to Oracle...
 Oracle connected successfully.
============================================================
 MAIN MENU
============================================================
 1. Student Login
 2. Admin Panel
 0. Exit
 Choice: 1
──────────────────────────────────────────────────────
 STUDENT LOGIN
──────────────────────────────────────────────────────
 Student ID : 41240202189
 Password   : ******
 Login successful! Welcome, Arman.

 AVAILABLE COURSES
──────────────────────────────────────────────────────
 ID   Course Name            Credits   Faculty
 ──────────────────────────────────────────────────
 2    Database Management    3         Dr. Islam
 3    Digital Electronics    3         Dr. Hossain
 4    Object Oriented Prog   3         Dr. Rahman
 5    Computer Networks      3         Dr. Islam
 [Completed courses are automatically hidden]

 Enter Course ID to register (0 to cancel): 2
 Successfully registered for "Database Management"!
```

## Getting started

**Requirements:** Python 3.9+, Oracle Database (XE or 21c), Oracle Instant Client

```bash
git clone https://github.com/armanbin007/Course-Registration-System.git
cd Course-Registration-System
```

### Step 1 — Set up the Oracle database (run once)

Open SQL*Plus and run the provided setup script:

```sql
@oracle_setup.sql
```

This creates all 5 tables, sequences, and sample data.

**Demo student login:** ID `41240202189` / Password `12345`

### Step 2 — Install Oracle Instant Client (if not already installed)

The Oracle driver needs Instant Client to talk to the database.

1. Download it from [Oracle's Instant Client page](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
2. Extract it (e.g. to `C:\oracle\instantclient_21_9`)
3. Add that folder to your Windows PATH

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure your `.env` file

Open `.env` and set your connection details.

If using `sqlplus / as sysdba` (most common for local Oracle XE):
```env
DB_USER=
DB_PASSWORD=
DB_DSN=localhost:1521/orcl
DB_MODE=sysdba
```

If using a normal Oracle user (e.g. `system`/`oracle123`):
```env
DB_USER=system
DB_PASSWORD=oracle123
DB_DSN=localhost:1521/orcl
DB_MODE=default
```

### Step 5 — Run the project

```bash
python main.py
```

## Usage

1. From the main menu, choose **Student Login** or **Admin Panel**
2. As a student: log in, browse the auto-filtered course list, register or drop a course
3. As an admin: add new students or mark a student's course as completed — this immediately updates what that student sees in their course list
4. All actions are committed to Oracle in real time, so progress persists across sessions

## Author

Built by [Arman Bin Alauddin](https://github.com/armanbin007) as a DBMS course project — Python + Oracle 21c, designed and implemented end-to-end.
