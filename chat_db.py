# Archivo: /var/www/dipa/bot/chat_db.py
import sqlite3
import os

DB_PATH = "chat_history.db"

def init_db():
    """Crea la base de datos y la tabla si no existen."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mensajes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id TEXT,
                  rol TEXT,
                  mensaje TEXT,
                  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def guardar_mensaje(session_id: str, rol: str, mensaje: str):
    """Guarda un mensaje en el historial."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO mensajes (session_id, rol, mensaje) VALUES (?, ?, ?)", (session_id, rol, mensaje))
    conn.commit()
    conn.close()

def obtener_historial(session_id: str):
    """Devuelve el historial de un usuario específico para recargar la página."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT rol, mensaje FROM mensajes WHERE session_id = ? ORDER BY id ASC", (session_id,))
    filas = c.fetchall()
    conn.close()
    return filas

def obtener_todos_los_mensajes():
    """Para el panel Admin: devuelve los últimos 500 mensajes de todos los usuarios."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT session_id, rol, mensaje, fecha FROM mensajes ORDER BY fecha DESC LIMIT 500")
    filas = c.fetchall()
    conn.close()
    return filas

# Inicializamos la DB apenas se importe este archivo
init_db()