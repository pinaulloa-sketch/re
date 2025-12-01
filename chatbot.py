"""
Módulo del chatbot con integración a Groq
"""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq
import database as db

# Cargar variables de entorno
load_dotenv()

class ChatBot:
    """Clase para gestionar el chatbot con Groq"""
    
    def __init__(self):
        """Inicializa el cliente de Groq"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or api_key == 'tu_api_key_aqui':
            raise ValueError(
                "Por favor configura tu GROQ_API_KEY en el archivo .env\n"
                "Obtén una API key gratis en: https://console.groq.com/keys"
            )
        
        self.client = Groq(api_key=api_key)
        # Usando Llama 3.1 70B - Modelo potente y gratuito
        self.model = "llama-3.1-8b-instant"
    
    def build_chat_context(self, user_id: int) -> List[Dict]:
        """
        Construye el contexto de chat para Groq
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de mensajes formateados para Groq
        """
        history = db.get_user_conversations(user_id)
        
        # Groq usa formato OpenAI compatible
        chat_history = []
        for msg in history:
            chat_history.append({
                'role': msg['role'] if msg['role'] == 'user' else 'assistant',
                'content': msg['content']
            })
        
        return chat_history
    
    def send_message(self, user_id: int, message: str) -> str:
        """
        Envía un mensaje al chatbot y obtiene la respuesta
        
        Args:
            user_id: ID del usuario
            message: Mensaje del usuario
            
        Returns:
            Respuesta del chatbot
        """
        # Guardar el mensaje del usuario
        db.save_message(user_id, 'user', message)
        
        # Obtener contexto de la conversación
        chat_history = self.build_chat_context(user_id)
        
        try:
            # Llamar a la API de Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_history,
                temperature=0.7,
                max_tokens=1024,
            )
            
            response_text = response.choices[0].message.content
            
            # Guardar respuesta del asistente
            db.save_message(user_id, 'assistant', response_text)
            
            return response_text
        
        except Exception as e:
            error_message = f"Error al comunicarse con Groq: {str(e)}"
            print(error_message)
            return f"Lo siento, ocurrió un error: {str(e)}"
    
    def clear_history(self, user_id: int):
        """
        Limpia el historial de conversación de un usuario
        
        Args:
            user_id: ID del usuario
        """
        db.clear_user_conversations(user_id)
    
    def get_conversation_summary(self, user_id: int) -> Dict:
        """
        Obtiene un resumen de la conversación del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con estadísticas de la conversación
        """
        count = db.get_conversation_count(user_id)
        conversations = db.get_user_conversations(user_id, limit=1)
        
        return {
            'total_messages': count,
            'has_history': count > 0,
            'last_message': conversations[-1] if conversations else None
        }
