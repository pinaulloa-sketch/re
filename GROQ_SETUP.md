# 🚀 Configuración de Groq para el Chatbot

## ✅ Migración Completada: Gemini → Groq

La aplicación ahora usa **Groq** en lugar de Google Gemini porque:
- ✅ **Tier gratuito más generoso** (sin límites tan estrictos)
- ✅ **Respuestas ultra rápidas** (hasta 10x más rápido)
- ✅ **Modelos potentes gratuitos** (Llama 3.1 70B)
- ✅ **Sin cuotas agotadas**

---

## 🔑 Configurar tu API Key de Groq

### Paso 1: Obtener la API Key

1. Ve a: **https://console.groq.com/keys**
2. Crea una cuenta gratis (si no tienes)
3. Haz clic en "Create API Key"
4. Copia la clave (empieza con `gsk_...`)

### Paso 2: Actualizar el archivo .env

Edita el archivo `.env` y reemplaza todo su contenido con:

```env
# Groq API Key
GROQ_API_KEY=tu_clave_aqui
```

**Ejemplo:**
```env
GROQ_API_KEY=gsk_abcd1234efgh5678ijkl
```

---

## 🤖 Modelo Utilizado

**Llama 3.1 70B Versatile**
- Modelo muy potente de Meta
- Gratis en Groq
- Excelente para conversaciones
- Respuestas rápidas y precisas

---

## ▶️ Ejecutar la Aplicación

```bash
python main.py
```

---

## 🎯 Ventajas de Groq

| Característica | Gemini Free | Groq Free |
|---------------|-------------|-----------|
| Velocidad | Normal | **Ultra rápido** |
| Límite diario | Muy bajo | **Muy generoso** |
| Modelos | gemini-pro | **Llama 3.1 70B** |
| Cuota | Se agota fácil | **Difícil de agotar** |

---

## 📝 Cambios Realizados

1. ✅ `requirements.txt` - Cambiado `google-generativeai` → `groq`
2. ✅ `chatbot.py` - Reescrito para API de Groq
3. ✅ `.env` - Configuración para `GROQ_API_KEY`
4. ✅ Instalado paquete `groq`

---

## 🆘 Solución de Problemas

### Error: "GROQ_API_KEY not found"
→ Verifica que editaste el archivo `.env` con tu clave real

### Error de autenticación
→ Asegúrate que copiaste la clave completa desde Groq Console

### El bot no responde
→ Verifica tu conexión a internet y que la API key sea válida

---

## 🎉 ¡Listo para usar!

Una vez configurada tu GROQ_API_KEY, ejecuta:
```bash
python main.py
```

Login con: `admin` / `admin123`

Y disfruta de conversaciones **ultra rápidas** con Llama 3.1! 🚀
