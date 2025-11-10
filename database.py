import sqlite3
from datetime import datetime

DB_NAME = "chat_history.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """    
    )
    conn.commit()
    conn.close()

def save_message(user_id, username, prompt, response):
    conn = get_connection() #variable para traer la conexion de la DB
    cursor = conn.cursor() #variable para seleccionar acciones
    cursor.execute(
        """
        INSERT INTO history(user_id, username, prompt, response, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, prompt, response, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=5):
    conn = get_connection() #variable para traer la conexion de la DB
    cursor = conn.cursor() #variable para seleccionar acciones
    cursor.execute( 
            """
            SELECT prompt, response, timestamp
            FROM history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """, (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows