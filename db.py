# db.py  —  Oracle connection handler
# ─────────────────────────────────────────────────────────────
# Reads credentials from .env and returns a oracledb connection.
# Every other module calls get_connection() from here.
# ─────────────────────────────────────────────────────────────

import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Returns an active oracledb connection.
    Mode is controlled by DB_MODE in .env:
      sysdba   → connects as SYSDBA (sqlplus / as sysdba)
      default  → normal user/password login
    """
    mode     = os.getenv("DB_MODE", "sysdba").strip().lower()
    user     = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()
    dsn      = os.getenv("DB_DSN", "localhost:1521/orcl").strip()

    try:
        if mode == "sysdba":
            conn = oracledb.connect(
                user     = "/",
                password = "",
                dsn      = dsn,
                mode     = oracledb.SYSDBA
            )
        else:
            conn = oracledb.connect(
                user     = user,
                password = password,
                dsn      = dsn
            )
        return conn

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"\n  [DB ERROR] Could not connect to Oracle.")
        print(f"  Code   : {error.code}")
        print(f"  Message: {error.message}")
        print(f"\n  Check your .env file and make sure Oracle is running.\n")
        raise SystemExit(1)


def test_connection():
    """Quick connectivity check used at startup."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 'OK' FROM DUAL")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] == "OK"
