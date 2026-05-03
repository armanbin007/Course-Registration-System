╔══════════════════════════════════════════════════════════════╗
║        COURSE REGISTRATION SYSTEM — Setup Guide             ║
║        Python + Oracle Database                              ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 1 — Set up the Oracle database (run ONCE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open Command Prompt and run:

    sqlplus / as sysdba @oracle_setup.sql

This creates all 5 tables + sequences + sample data.
Demo student: ID = 1  |  Password = 1234


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 2 — Install Oracle Instant Client (if not already done)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cx_Oracle needs Oracle Instant Client to talk to the database.
Download from: https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html

Extract it (e.g. to C:\oracle\instantclient_21_9)
Then add that folder to your Windows PATH.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 3 — Install Python dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    pip install -r requirements.txt


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 4 — Edit the .env file
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open .env and set your connection details.

If you use "sqlplus / as sysdba" (most common for local Oracle XE):
    DB_USER=
    DB_PASSWORD=
    DB_DSN=localhost:1521/XE
    DB_MODE=sysdba

If you have a normal Oracle user (e.g. scott/tiger):
    DB_USER=scott
    DB_PASSWORD=tiger
    DB_DSN=localhost:1521/XE
    DB_MODE=default


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 5 — Run the project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    python main.py


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Project File Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

course_reg_python/
├── main.py            ← Entry point, all menus
├── db.py              ← Oracle connection handler
├── auth.py            ← Student login
├── courses.py         ← View available/all courses
├── enrollment.py      ← Register, drop, view, completed
├── admin.py           ← Admin panel
├── oracle_setup.sql   ← Run this in SQL*Plus first
├── requirements.txt   ← Python packages
├── .env               ← Your DB credentials (don't share this)
└── README.txt         ← This file


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Demo credentials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Student login:  ID = 1   |  Password = 1234
Admin panel:    PIN = admin123

"Data Structures" is pre-marked as completed for student 1
so you can immediately demo the course-blocking feature.
