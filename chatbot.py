import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq
import database as bd

load_dotenv()

class ChatBotIA:
    
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or api_key == 'tu_api_key_aqui':
            raise ValueError(
                "Por favor configura tu GROQ_API_KEY en el archivo .env\n"
                "Obtén una API key gratis en: https://console.groq.com/keys"
            )
        
        self.cliente = Groq(api_key=api_key)
        self.modelo = "llama-3.1-8b-instant"
    
    def construir_contexto_chat(self, id_usuario: int) -> List[Dict]:
        historial = bd.obtener_conversaciones_usuario(id_usuario)
        
        historial_chat = []
        for mensaje in historial:
            historial_chat.append({
                'role': mensaje['role'] if mensaje['role'] == 'user' else 'assistant',
                'content': mensaje['content']
            })
        
        return historial_chat
    
    def enviar_mensaje(self, id_usuario: int, mensaje: str) -> str:
        bd.guardar_mensaje(id_usuario, 'user', mensaje)
        
        historial_chat = self.construir_contexto_chat(id_usuario)
        
        try:
            respuesta = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=historial_chat,
                temperature=0.7,
                max_tokens=1024,
            )
            
            texto_respuesta = respuesta.choices[0].message.content
            
            bd.guardar_mensaje(id_usuario, 'assistant', texto_respuesta)
            
            return texto_respuesta
        
        except Exception as e:
            mensaje_error = f"Error al comunicarse con Groq: {str(e)}"
            print(mensaje_error)
            return f"Lo siento, ocurrió un error: {str(e)}"
    
    def limpiar_historial(self, id_usuario: int):
        bd.limpiar_conversaciones_usuario(id_usuario)
    
    def obtener_resumen_conversacion(self, id_usuario: int) -> Dict:
        cantidad = bd.obtener_cantidad_conversaciones(id_usuario)
        conversaciones = bd.obtener_conversaciones_usuario(id_usuario, limite=1)
        
        return {
            'total_mensajes': cantidad,
            'tiene_historial': cantidad > 0,
            'ultimo_mensaje': conversaciones[-1] if conversaciones else None
        }
