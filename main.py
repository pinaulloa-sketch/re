"""
Aplicación de Chatbot Multi-Usuario con Flet
"""
import flet as ft
from typing import Optional
import database as db
import auth
from chatbot import ChatBot

class ChatApp:
    """Aplicación principal del chatbot"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user: Optional[dict] = None
        self.chatbot: Optional[ChatBot] = None
        
        # Configuración de la página
        self.page.title = "Chatbot Multi-Usuario"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_resizable = True
        
        # Inicializar base de datos
        try:
            db.init_database()
            auth.create_default_user()
        except Exception as e:
            print(f"Error al inicializar base de datos: {e}")
        
        # Mostrar pantalla de login
        self.show_login_screen()
    
    def show_login_screen(self):
        """Muestra la pantalla de inicio de sesión"""
        self.page.controls.clear()
        
        # Campos de entrada
        self.username_field = ft.TextField(
            label="Usuario",
            width=300,
            autofocus=True,
            on_submit=lambda _: self.login()
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            on_submit=lambda _: self.login()
        )
        
        # Mensaje de error/éxito
        self.login_message = ft.Text("", color=ft.Colors.RED, size=14)
        
        # Contenedor principal
        login_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=80, color=ft.Colors.BLUE),
                    ft.Container(height=20),
                    ft.Text(
                        "Chatbot Multi-Usuario",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Inicia sesión para continuar",
                        size=16,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    self.username_field,
                    self.password_field,
                    self.login_message,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Iniciar Sesión",
                        width=300,
                        on_click=lambda _: self.login(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.Container(height=10),
                    ft.TextButton(
                        "¿No tienes cuenta? Regístrate",
                        on_click=lambda _: self.show_register_screen()
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Usuario de prueba: admin / admin123",
                        size=12,
                        color=ft.Colors.GREY_600,
                        italic=True,
                        text_align=ft.TextAlign.CENTER
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )
        
        self.page.add(login_container)
        self.page.update()
    
    def show_register_screen(self):
        """Muestra la pantalla de registro"""
        self.page.controls.clear()
        
        # Campos de entrada
        self.reg_username_field = ft.TextField(
            label="Usuario (mínimo 3 caracteres)",
            width=300,
            autofocus=True
        )
        
        self.reg_password_field = ft.TextField(
            label="Contraseña (mínimo 4 caracteres)",
            width=300,
            password=True,
            can_reveal_password=True
        )
        
        self.reg_password_confirm_field = ft.TextField(
            label="Confirmar contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            on_submit=lambda _: self.register()
        )
        
        # Mensaje de error/éxito
        self.register_message = ft.Text("", size=14)
        
        # Contenedor principal
        register_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=80, color=ft.Colors.GREEN),
                    ft.Container(height=20),
                    ft.Text(
                        "Crear Nueva Cuenta",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    self.reg_username_field,
                    self.reg_password_field,
                    self.reg_password_confirm_field,
                    self.register_message,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Registrarse",
                        width=300,
                        on_click=lambda _: self.register(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.Container(height=10),
                    ft.TextButton(
                        "¿Ya tienes cuenta? Inicia sesión",
                        on_click=lambda _: self.show_login_screen()
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )
        
        self.page.add(register_container)
        self.page.update()
    
    def login(self):
        """Intenta iniciar sesión con las credenciales proporcionadas"""
        username = self.username_field.value
        password = self.password_field.value
        
        success, message, user = auth.login_user(username, password)
        
        if success:
            self.current_user = user
            self.login_message.value = ""
            self.show_chat_screen()
        else:
            self.login_message.value = message
            self.login_message.color = ft.Colors.RED
            self.page.update()
    
    def register(self):
        """Registra un nuevo usuario"""
        username = self.reg_username_field.value
        password = self.reg_password_field.value
        password_confirm = self.reg_password_confirm_field.value
        
        # Validar que las contraseñas coincidan
        if password != password_confirm:
            self.register_message.value = "Las contraseñas no coinciden"
            self.register_message.color = ft.Colors.RED
            self.page.update()
            return
        
        success, message, user_id = auth.register_user(username, password)
        
        if success:
            self.register_message.value = f"{message}. Redirigiendo al login..."
            self.register_message.color = ft.Colors.GREEN
            self.page.update()
            
            # Esperar un momento y redirigir al login
            import time
            time.sleep(1.5)
            self.show_login_screen()
        else:
            self.register_message.value = message
            self.register_message.color = ft.Colors.RED
            self.page.update()
    
    def show_chat_screen(self):
        """Muestra la interfaz de chat"""
        self.page.controls.clear()
        
        # Inicializar chatbot
        try:
            self.chatbot = ChatBot()
        except ValueError as e:
            # Si no hay API key configurada
            error_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error de Configuración"),
                content=ft.Text(str(e)),
                actions=[
                    ft.TextButton("OK", on_click=lambda _: self.page.close(error_dialog))
                ],
            )
            self.page.overlay.append(error_dialog)
            error_dialog.open = True
            self.page.update()
            self.logout()
            return
        
        # Contenedor de mensajes
        self.chat_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True,
        )
        
        # Cargar historial de conversaciones
        self.load_chat_history()
        
        # Campo de entrada de mensaje
        self.message_field = ft.TextField(
            hint_text="Escribe tu mensaje aquí...",
            expand=True,
            multiline=True,
            max_lines=3,
            shift_enter=True,
            on_submit=lambda _: self.send_message()
        )
        
        # Botón de envío
        self.send_button = ft.IconButton(
            icon=ft.Icons.SEND,
            tooltip="Enviar mensaje",
            on_click=lambda _: self.send_message()
        )
        
        # Indicador de estado
        self.status_text = ft.Text("", size=12, italic=True, color=ft.Colors.GREY_600)
        
        # Barra superior
        top_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=30),
                    ft.Text(
                        f"Usuario: {self.current_user['username']}",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="Limpiar conversación",
                        on_click=lambda _: self.clear_conversation()
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        tooltip="Cerrar sesión",
                        on_click=lambda _: self.logout()
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLUE_200)),
        )
        
        # Área de entrada
        input_area = ft.Container(
            content=ft.Column(
                [
                    self.status_text,
                    ft.Row(
                        [
                            self.message_field,
                            self.send_button,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=5,
            ),
            padding=15,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
        
        # Layout principal
        main_layout = ft.Column(
            [
                top_bar,
                ft.Container(
                    content=self.chat_list,
                    expand=True,
                    bgcolor=ft.Colors.GREY_50,
                ),
                input_area,
            ],
            spacing=0,
            expand=True,
        )
        
        self.page.add(main_layout)
        self.page.update()
    
    def load_chat_history(self):
        """Carga el historial de chat del usuario actual"""
        if not self.current_user:
            return
        
        conversations = db.get_user_conversations(self.current_user['id'])
        
        for msg in conversations:
            self.add_message_to_ui(msg['role'], msg['content'], save=False)
    
    def add_message_to_ui(self, role: str, content: str, save: bool = True):
        """
        Agrega un mensaje a la interfaz
        
        Args:
            role: 'user' o 'assistant'
            content: Contenido del mensaje
            save: Si se debe guardar en la base de datos
        """
        is_user = role == 'user'
        
        message_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.PERSON if is_user else ft.Icons.SMART_TOY,
                                size=20,
                                color=ft.Colors.BLUE if is_user else ft.Colors.GREEN
                            ),
                            ft.Text(
                                "Tú" if is_user else "Asistente",
                                weight=ft.FontWeight.BOLD,
                                size=14,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Container(
                        content=ft.Text(content, selectable=True),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_100 if is_user else ft.Colors.GREEN_100,
                        border_radius=10,
                    ),
                ],
                spacing=5,
            ),
            padding=ft.padding.only(left=10 if is_user else 0, right=0 if is_user else 10),
        )
        
        self.chat_list.controls.append(message_container)
        self.page.update()
    
    def send_message(self):
        """Envía un mensaje al chatbot"""
        message = self.message_field.value.strip()
        
        if not message:
            return
        
        # Limpiar campo de entrada
        self.message_field.value = ""
        self.message_field.focus()
        
        # Deshabilitar botón de envío
        self.send_button.disabled = True
        self.status_text.value = "Enviando mensaje..."
        self.page.update()
        
        # Mostrar mensaje del usuario
        self.add_message_to_ui('user', message, save=False)
        
        # Obtener respuesta del chatbot
        self.status_text.value = "El asistente está escribiendo..."
        self.page.update()
        
        try:
            response = self.chatbot.send_message(self.current_user['id'], message)
            self.add_message_to_ui('assistant', response, save=False)
            self.status_text.value = ""
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.add_message_to_ui('assistant', error_msg, save=False)
            self.status_text.value = ""
        
        # Habilitar botón de envío
        self.send_button.disabled = False
        self.page.update()
    
    def clear_conversation(self):
        """Limpia la conversación del usuario actual"""
        def confirm_clear(e):
            if e.control.text == "Sí":
                if self.chatbot:
                    self.chatbot.clear_history(self.current_user['id'])
                self.chat_list.controls.clear()
                self.page.update()
            self.page.close(dialog)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Estás seguro de que deseas eliminar toda la conversación?"),
            actions=[
                ft.TextButton("Sí", on_click=confirm_clear),
                ft.TextButton("No", on_click=lambda _: self.page.close(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def logout(self):
        """Cierra la sesión del usuario actual"""
        self.current_user = None
        self.chatbot = None
        self.show_login_screen()

def main(page: ft.Page):
    """Función principal de la aplicación"""
    ChatApp(page)

if __name__ == "__main__":
    ft.app(target=main)
