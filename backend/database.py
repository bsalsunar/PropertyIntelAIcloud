import sqlite3
import json
from datetime import datetime

DB_PATH = "realestate.db"


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        listing_text TEXT,
        quality_score INTEGER,
        seo_score INTEGER,
        completeness_score INTEGER,
        missing_fields TEXT,
        explanation TEXT,
        seo_keywords TEXT,
        improvement_suggestions TEXT,
        improved_listing TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_analysis(listing_text: str, result: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analysis_results (
        listing_text,
        quality_score,
        seo_score,
        completeness_score,
        missing_fields,
        explanation,
        seo_keywords,
        improvement_suggestions,
        improved_listing,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        listing_text,
        result.get("quality_score"),
        result.get("seo_score"),
        result.get("completeness_score"),
        json.dumps(result.get("missing_fields", [])),
        json.dumps(result.get("explanation", [])),
        json.dumps(result.get("seo_keywords", [])),
        json.dumps(result.get("improvement_suggestions", [])),
        result.get("improved_listing", ""),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
