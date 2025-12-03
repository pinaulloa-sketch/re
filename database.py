import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

NOMBRE_BD = "chatbot.db"

def inicializar_base_datos():
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    
    with open('database_schema.sql', 'r', encoding='utf-8') as f:
        esquema = f.read()
        cursor.executescript(esquema)
    
    conexion.commit()
    conexion.close()
    print("Base de datos inicializada correctamente")

def obtener_conexion():
    conexion = sqlite3.connect(NOMBRE_BD)
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_usuario(nombre_usuario: str, hash_contrasena: str) -> Optional[int]:
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (nombre_usuario, hash_contrasena)
        )
        id_usuario = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return id_usuario
    except sqlite3.IntegrityError:
        return None

def obtener_usuario_por_nombre(nombre_usuario: str) -> Optional[dict]:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (nombre_usuario,))
    fila = cursor.fetchone()
    conexion.close()
    
    if fila:
        return {
            'id': fila['id'],
            'username': fila['username'],
            'password_hash': fila['password_hash'],
            'created_at': fila['created_at']
        }
    return None

def obtener_todos_usuarios() -> List[dict]:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, username, created_at FROM users")
    filas = cursor.fetchall()
    conexion.close()
    
    return [
        {
            'id': fila['id'],
            'username': fila['username'],
            'created_at': fila['created_at']
        }
        for fila in filas
    ]

def eliminar_usuario(id_usuario: int) -> bool:
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM conversations WHERE user_id = ?", (id_usuario,))
        cursor.execute("DELETE FROM users WHERE id = ?", (id_usuario,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False

def guardar_mensaje(id_usuario: int, rol: str, contenido: str):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
        (id_usuario, rol, contenido)
    )
    conexion.commit()
    conexion.close()

def obtener_conversaciones_usuario(id_usuario: int, limite: Optional[int] = None) -> List[dict]:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    consulta = """
        SELECT role, content, timestamp 
        FROM conversations 
        WHERE user_id = ? 
        ORDER BY timestamp ASC
    """
    
    if limite:
        consulta += f" LIMIT {limite}"
    
    cursor.execute(consulta, (id_usuario,))
    filas = cursor.fetchall()
    conexion.close()
    
    return [
        {
            'role': fila['role'],
            'content': fila['content'],
            'timestamp': fila['timestamp']
        }
        for fila in filas
    ]

def limpiar_conversaciones_usuario(id_usuario: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM conversations WHERE user_id = ?", (id_usuario,))
    conexion.commit()
    conexion.close()

def obtener_cantidad_conversaciones(id_usuario: int) -> int:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM conversations WHERE user_id = ?", (id_usuario,))
    fila = cursor.fetchone()
    conexion.close()
    return fila['count']
