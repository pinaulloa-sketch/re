# Chatbot Multi-Usuario - Archivo README

## Descripción
Aplicación de escritorio con interfaz gráfica en Flet que permite a múltiples usuarios iniciar sesión y mantener conversaciones independientes con un chatbot basado en **Groq (Llama 3.1 70B)**. Cada usuario tiene su propio historial de conversación almacenado en SQLite.

## Características
- ✅ Autenticación de usuarios con contraseñas hasheadas (bcrypt)
- ✅ Registro de nuevos usuarios
- ✅ Base de datos SQLite para persistencia
- ✅ Integración con **Groq API** (ultra rápido y gratuito)
- ✅ Modelo **Llama 3.1 70B Versatile** - Potente y gratis
- ✅ Memoria de conversación individual por usuario
- ✅ Interfaz gráfica moderna con Flet
- ✅ Historial de conversaciones persistente

## Requisitos Previos
- Python 3.8 o superior
- API Key de Google Gemini (obtener en: https://makersuite.google.com/app/apikey)

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key
Edita el archivo `.env` y agrega tu API key de Google Gemini:
```
GEMINI_API_KEY=tu_api_key_real_aqui
```

### 3. Ejecutar la aplicación
```bash
python main.py
```

## Uso

### Primer inicio
La aplicación crea automáticamente un usuario de prueba:
- **Usuario:** admin
- **Contraseña:** admin123

### Crear nuevos usuarios
1. En la pantalla de login, haz clic en "¿No tienes cuenta? Regístrate"
2. Completa el formulario con:
   - Usuario (mínimo 3 caracteres)
   - Contraseña (mínimo 4 caracteres)
   - Confirmación de contraseña
3. Haz clic en "Registrarse"

### Iniciar conversación
1. Inicia sesión con tus credenciales
2. Escribe tu mensaje en el campo de texto
3. Presiona Enter o haz clic en el botón de envío
4. El chatbot responderá usando Google Gemini

### Funciones adicionales
- **Limpiar conversación:** Haz clic en el ícono de papelera en la barra superior
- **Cerrar sesión:** Haz clic en el ícono de logout

## Estructura del Proyecto
```
chatbot-app/
├── main.py                  # Aplicación principal con interfaz Flet
├── database.py              # Gestión de base de datos SQLite
├── database_schema.sql      # Esquema de la base de datos
├── auth.py                  # Módulo de autenticación
├── chatbot.py               # Integración con Google Gemini
├── .env                     # Configuración de API key
├── requirements.txt         # Dependencias del proyecto
├── chatbot.db              # Base de datos SQLite (se crea automáticamente)
└── README.md               # Este archivo
```

## Características Técnicas

### Base de Datos
- **usuarios:** Almacena credenciales y datos de usuarios
- **conversaciones:** Almacena mensajes con relación a usuarios

### Seguridad
- Contraseñas hasheadas con bcrypt
- API key almacenada en variable de entorno
- Validación de usuarios y contraseñas

### Memoria de Conversación
- Cada usuario tiene su propio historial
- Las conversaciones persisten entre sesiones
- El chatbot mantiene contexto de conversaciones anteriores

## Solución de Problemas

### Error: "Por favor configura tu GEMINI_API_KEY"
- Verifica que el archivo `.env` existe
- Asegúrate de que la API key esté configurada correctamente
- La API key no debe ser "tu_api_key_aqui"

### Error al inicializar la base de datos
- Verifica que el archivo `database_schema.sql` existe
- Asegúrate de tener permisos de escritura en el directorio

### El chatbot no responde
- Verifica tu conexión a internet
- Confirma que tu API key de Gemini es válida
- Revisa que no hayas excedido el límite de la API

## Notas
- La aplicación usa el modelo `gemini-pro` de Google
- Las conversaciones se almacenan localmente en `chatbot.db`
- Se recomienda cambiar la contraseña del usuario admin por defecto
