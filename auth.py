"""
Módulo de autenticación de usuarios
"""
import bcrypt
from typing import Optional, Tuple
import database as db

def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando bcrypt
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash de la contraseña
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica que una contraseña coincida con su hash
    
    Args:
        password: Contraseña en texto plano
        password_hash: Hash almacenado
        
    Returns:
        True si coincide, False en caso contrario
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(username: str, password: str) -> Tuple[bool, str, Optional[int]]:
    """
    Registra un nuevo usuario
    
    Args:
        username: Nombre de usuario
        password: Contraseña
        
    Returns:
        Tupla (éxito, mensaje, user_id)
    """
    # Validar username
    if not username or len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres", None
    
    # Validar password
    if not password or len(password) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres", None
    
    # Verificar si el usuario ya existe
    existing_user = db.get_user_by_username(username)
    if existing_user:
        return False, "El nombre de usuario ya está en uso", None
    
    # Crear usuario
    password_hash = hash_password(password)
    user_id = db.create_user(username, password_hash)
    
    if user_id:
        return True, "Usuario registrado exitosamente", user_id
    else:
        return False, "Error al crear el usuario", None

def login_user(username: str, password: str) -> Tuple[bool, str, Optional[dict]]:
    """
    Autentica un usuario
    
    Args:
        username: Nombre de usuario
        password: Contraseña
        
    Returns:
        Tupla (éxito, mensaje, datos_usuario)
    """
    # Validar campos
    if not username or not password:
        return False, "Por favor ingrese usuario y contraseña", None
    
    # Buscar usuario
    user = db.get_user_by_username(username)
    if not user:
        return False, "Usuario o contraseña incorrectos", None
    
    # Verificar contraseña
    if verify_password(password, user['password_hash']):
        return True, "Login exitoso", user
    else:
        return False, "Usuario o contraseña incorrectos", None

def create_default_user():
    """Crea un usuario admin por defecto si no existe"""
    default_username = "admin"
    default_password = "admin123"
    
    existing_user = db.get_user_by_username(default_username)
    if not existing_user:
        success, message, user_id = register_user(default_username, default_password)
        if success:
            print(f"Usuario por defecto creado: {default_username} / {default_password}")
            return True
    return False
