╔══════════════════════════════════════════════════════════════╗
║        COURSE REGISTRATION SYSTEM — Setup Guide             ║
║        Python + Oracle Database                              ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 1 — Set up the Oracle database (run ONCE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open SQL Plus and run:

    @oracle_setup.sql

This creates all 5 tables + sequences + sample data.
Demo student: ID = 41240202189  |  Password = 12345


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
    DB_DSN=localhost:1521/orcl
    DB_MODE=sysdba

If you have a normal Oracle user (e.g. system/oracle123):
    DB_USER=system
    DB_PASSWORD=oracle123
    DB_DSN=localhost:1521/orcl
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

Student login:  ID = 41240202189   |  Password = 12345
Admin panel:    PIN = admin123

"Data Structures" is pre-marked as completed for student 41240202189
so you can immediately demo the course-blocking feature.
