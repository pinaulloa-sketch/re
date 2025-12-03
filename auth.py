import bcrypt
from typing import Optional, Tuple
import database as bd

def generar_hash_contrasena(contrasena: str) -> str:
    sal = bcrypt.gensalt()
    hash_generado = bcrypt.hashpw(contrasena.encode('utf-8'), sal)
    return hash_generado.decode('utf-8')

def verificar_contrasena(contrasena: str, hash_contrasena: str) -> bool:
    return bcrypt.checkpw(contrasena.encode('utf-8'), hash_contrasena.encode('utf-8'))

def registrar_usuario(nombre_usuario: str, contrasena: str) -> Tuple[bool, str, Optional[int]]:
    if not nombre_usuario or len(nombre_usuario) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres", None
    
    if not contrasena or len(contrasena) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres", None
    
    usuario_existente = bd.obtener_usuario_por_nombre(nombre_usuario)
    if usuario_existente:
        return False, "El nombre de usuario ya está en uso", None
    
    hash_contrasena = generar_hash_contrasena(contrasena)
    id_usuario = bd.crear_usuario(nombre_usuario, hash_contrasena)
    
    if id_usuario:
        return True, "Usuario registrado exitosamente", id_usuario
    else:
        return False, "Error al crear el usuario", None

def iniciar_sesion(nombre_usuario: str, contrasena: str) -> Tuple[bool, str, Optional[dict]]:
    if not nombre_usuario or not contrasena:
        return False, "Por favor ingrese usuario y contraseña", None
    
    usuario = bd.obtener_usuario_por_nombre(nombre_usuario)
    if not usuario:
        return False, "Usuario o contraseña incorrectos", None
    
    if verificar_contrasena(contrasena, usuario['password_hash']):
        return True, "Login exitoso", usuario
    else:
        return False, "Usuario o contraseña incorrectos", None

def crear_usuario_predeterminado():
    nombre_usuario_predeterminado = "admin"
    contrasena_predeterminada = "admin123"
    
    usuario_existente = bd.obtener_usuario_por_nombre(nombre_usuario_predeterminado)
    if not usuario_existente:
        exito, mensaje, id_usuario = registrar_usuario(nombre_usuario_predeterminado, contrasena_predeterminada)
        if exito:
            print(f"Usuario por defecto creado: {nombre_usuario_predeterminado} / {contrasena_predeterminada}")
            return True
    return False
