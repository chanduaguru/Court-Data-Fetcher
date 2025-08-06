# scraper/logger.py
import sqlite3
import os
from datetime import datetime

DB_NAME = "queries.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_number TEXT,
            filing_year TEXT,
            court_complex TEXT,
            response_html TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Automatically initialize DB on import
init_db()

def log_query(case_number, filing_year, court_complex, response_html):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO case_queries (case_number, filing_year, court_complex, response_html, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_number, filing_year, court_complex, response_html, timestamp))
    conn.commit()
    conn.close()
