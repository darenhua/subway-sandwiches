# backend/storage.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime

DB_PATH = Path(__file__).parent / "app.db"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            filename TEXT,
            text TEXT NOT NULL,
            meta_json TEXT
        );
        """)
        con.commit()

@contextmanager
def db():
    con = sqlite3.connect(DB_PATH)
    try:
        yield con
    finally:
        con.close()

def insert_transcript(filename: Optional[str], text: str, meta: Optional[Dict[str, Any]] = None) -> int:
    with db() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO transcripts (created_at, filename, text, meta_json) VALUES (?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), filename, text, json.dumps(meta or {})),
        )
        con.commit()
        return cur.lastrowid

def get_transcript(tid: int):
    with db() as con:
        cur = con.cursor()
        cur.execute("SELECT id, created_at, filename, text, meta_json FROM transcripts WHERE id = ?", (tid,))
        row = cur.fetchone()
        if not row: return None
        return {
            "id": row[0],
            "created_at": row[1],
            "filename": row[2],
            "text": row[3],
            "meta": json.loads(row[4]) if row[4] else {}
        }
