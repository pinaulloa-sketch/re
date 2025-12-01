"""
Módulo de gestión de base de datos SQLite
"""
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

DB_NAME = "chatbot.db"

def init_database():
    """Inicializa la base de datos creando las tablas necesarias"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Leer y ejecutar el schema SQL
    with open('database_schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

def get_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ========== Funciones para usuarios ==========

def create_user(username: str, password_hash: str) -> Optional[int]:
    """
    Crea un nuevo usuario
    
    Args:
        username: Nombre de usuario
        password_hash: Hash de la contraseña
        
    Returns:
        ID del usuario creado o None si ya existe
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None

def get_user_by_username(username: str) -> Optional[dict]:
    """
    Obtiene un usuario por su nombre
    
    Args:
        username: Nombre de usuario
        
    Returns:
        Diccionario con datos del usuario o None si no existe
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row['id'],
            'username': row['username'],
            'password_hash': row['password_hash'],
            'created_at': row['created_at']
        }
    return None

def get_all_users() -> List[dict]:
    """Obtiene todos los usuarios"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, created_at FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row['id'],
            'username': row['username'],
            'created_at': row['created_at']
        }
        for row in rows
    ]

# ========== Funciones para conversaciones ==========

def save_message(user_id: int, role: str, content: str):
    """
    Guarda un mensaje en la base de datos
    
    Args:
        user_id: ID del usuario
        role: Rol del mensaje ('user' o 'assistant')
        content: Contenido del mensaje
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
        (user_id, role, content)
    )
    conn.commit()
    conn.close()

def get_user_conversations(user_id: int, limit: Optional[int] = None) -> List[dict]:
    """
    Obtiene el historial de conversaciones de un usuario
    
    Args:
        user_id: ID del usuario
        limit: Límite de mensajes a obtener (None para todos)
        
    Returns:
        Lista de mensajes ordenados por timestamp
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT role, content, timestamp 
        FROM conversations 
        WHERE user_id = ? 
        ORDER BY timestamp ASC
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'role': row['role'],
            'content': row['content'],
            'timestamp': row['timestamp']
        }
        for row in rows
    ]

def clear_user_conversations(user_id: int):
    """
    Elimina todas las conversaciones de un usuario
    
    Args:
        user_id: ID del usuario
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_conversation_count(user_id: int) -> int:
    """
    Obtiene el número de mensajes de un usuario
    
    Args:
        user_id: ID del usuario
        
    Returns:
        Número de mensajes
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM conversations WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row['count']
