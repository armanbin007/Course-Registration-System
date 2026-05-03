BEGIN EXECUTE IMMEDIATE 'DROP TABLE ENROLLMENT       CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE COMPLETED_COURSE CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE COURSE           CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE STUDENT          CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE FACULTY          CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- Drop sequences
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_student';    EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_faculty';    EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_course';     EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_enrollment'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_completed';  EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- ── Sequences ────────────────────────────────────────────────
CREATE SEQUENCE seq_student    START WITH 41240202189 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_faculty    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_course     START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_enrollment START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_completed  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- ── Tables ────────────────────────────────────────────────────
CREATE TABLE FACULTY (
    faculty_id   NUMBER        PRIMARY KEY,
    faculty_name VARCHAR2(100) NOT NULL,
    department   VARCHAR2(50),
    email        VARCHAR2(100) UNIQUE NOT NULL
);

CREATE TABLE STUDENT (
    student_id       NUMBER        PRIMARY KEY,
    full_name        VARCHAR2(100) NOT NULL,
    email            VARCHAR2(100) UNIQUE NOT NULL,
    pass_word        VARCHAR2(100) NOT NULL,
    department       VARCHAR2(50),
    current_semester NUMBER,
    status           VARCHAR2(20) DEFAULT 'active'
                     CHECK (status IN ('active', 'suspended'))
);

CREATE TABLE COURSE (
    course_id    NUMBER        PRIMARY KEY,
    course_name  VARCHAR2(100) NOT NULL,
    credit_hours NUMBER        NOT NULL CHECK (credit_hours > 0),
    faculty_id   NUMBER        REFERENCES FACULTY(faculty_id),
    max_seats    NUMBER        DEFAULT 40,
    semester     VARCHAR2(20),
    year_val     VARCHAR2(10)
);

CREATE TABLE ENROLLMENT (
    enrollment_id NUMBER PRIMARY KEY,
    student_id    NUMBER REFERENCES STUDENT(student_id),
    course_id     NUMBER REFERENCES COURSE(course_id),
    enrolled_at   DATE DEFAULT SYSDATE,
    status        VARCHAR2(20) DEFAULT 'active'
                  CHECK (status IN ('active', 'dropped')),
    CONSTRAINT uq_enrollment UNIQUE (student_id, course_id)
);

CREATE TABLE COMPLETED_COURSE (
    record_id       NUMBER PRIMARY KEY,
    student_id      NUMBER REFERENCES STUDENT(student_id),
    course_id       NUMBER REFERENCES COURSE(course_id),
    grade           VARCHAR2(2) CHECK (grade IN ('A','B','C','D','F')),
    completion_date DATE DEFAULT SYSDATE
);

-- ── Seed Data ─────────────────────────────────────────────────
INSERT INTO FACULTY VALUES (seq_faculty.NEXTVAL, 'Dr. Rahman',  'CSE', 'rahman@nub.edu');
INSERT INTO FACULTY VALUES (seq_faculty.NEXTVAL, 'Dr. Hossain', 'EEE', 'hossain@unubnnubi.edu');
INSERT INTO FACULTY VALUES (seq_faculty.NEXTVAL, 'Dr. Islam',   'CSE', 'islam@nub.edu');

INSERT INTO COURSE VALUES (seq_course.NEXTVAL, 'Data Structures',      3, 1, 40, 'Summer', '2026');
INSERT INTO COURSE VALUES (seq_course.NEXTVAL, 'Database Management System',  3, 3, 35, 'Summer', '2026');
INSERT INTO COURSE VALUES (seq_course.NEXTVAL, 'Digital Electronics',  3, 2, 30, 'Summer', '2026');
INSERT INTO COURSE VALUES (seq_course.NEXTVAL, 'Object Oriented Programming', 3, 1, 40, 'Summer', '2026');
INSERT INTO COURSE VALUES (seq_course.NEXTVAL, 'Computer Networks',    3, 3, 35, 'Summer', '2026');

-- Demo student: ID=1, password=12345
INSERT INTO STUDENT VALUES (seq_student.NEXTVAL, 'Arman', 'arman@nub.edu', '12345', 'CSE', 4, 'active');

-- Data Structures already completed by student 1 (to demo block feature)
INSERT INTO COMPLETED_COURSE VALUES (seq_completed.NEXTVAL, 41240202189, 1, 'A', DATE '2024-10-12');

COMMIT;

PROMPT ============================================================
PROMPT  Setup complete! Tables created and seed data inserted.
PROMPT  Demo login: Student ID = 41240202189  |  Password = 12345
PROMPT ============================================================
