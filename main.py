import flet as ft
from typing import Optional
import database as bd
import auth
from chatbot import ChatBotIA

class AplicacionChat:
    
    def __init__(self, pagina: ft.Page):
        self.pagina = pagina
        self.usuario_actual: Optional[dict] = None
        self.chatbot: Optional[ChatBotIA] = None
        
        self.pagina.title = "Chatbot Multi-Usuario"
        self.pagina.theme_mode = ft.ThemeMode.DARK
        self.pagina.padding = 0
        self.pagina.window_width = 900
        self.pagina.window_height = 700
        self.pagina.window_resizable = True
        self.pagina.fonts = {
            "Outfit": "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap"
        }
        self.pagina.theme = ft.Theme(font_family="Outfit")
        
        try:
            bd.inicializar_base_datos()
            auth.crear_usuario_predeterminado()
        except Exception as e:
            print(f"Error al inicializar base de datos: {e}")
        
        self.mostrar_pantalla_login()
    
    def mostrar_pantalla_login(self):
        self.pagina.controls.clear()
        
        self.campo_usuario = ft.TextField(
            label="Usuario",
            width=320,
            autofocus=True,
            on_submit=lambda _: self.iniciar_sesion(),
            border_radius=12,
            filled=True,
            bgcolor="#1a1a2e",
            border_color="#6C63FF",
            prefix_icon=ft.Icons.PERSON,
        )
        
        self.campo_contrasena = ft.TextField(
            label="Contraseña",
            width=320,
            password=True,
            can_reveal_password=True,
            on_submit=lambda _: self.iniciar_sesion(),
            border_radius=12,
            filled=True,
            bgcolor="#1a1a2e",
            border_color="#6C63FF",
            prefix_icon=ft.Icons.LOCK,
        )
        
        self.mensaje_login = ft.Text("", size=14)
        
        contenedor_login = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.CHAT_BUBBLE_ROUNDED, size=100, color="#6C63FF"),
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Chatbot Inteligente",
                        size=42,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color="#6C63FF",
                    ),
                    ft.Text(
                        "Tu asistente personal con IA",
                        size=18,
                        color="#8b8b8b",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=40),
                    self.campo_usuario,
                    ft.Container(height=10),
                    self.campo_contrasena,
                    self.mensaje_login,
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Iniciar Sesión",
                            width=320,
                            height=50,
                            on_click=lambda _: self.iniciar_sesion(),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                bgcolor="#6C63FF",
                                color="white",
                            ),
                        ),
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.Colors.with_opacity(0.3, "#6C63FF"),
                            offset=ft.Offset(0, 4),
                        ),
                    ),
                    ft.Container(height=15),
                    ft.TextButton(
                        "¿No tienes cuenta? Regístrate aquí",
                        on_click=lambda _: self.mostrar_pantalla_registro(),
                        style=ft.ButtonStyle(color="#6C63FF"),
                    ),
                    ft.Container(height=30),
                    ft.Container(
                        content=ft.Text(
                            "🔑 Usuario de prueba: admin / admin123",
                            size=13,
                            color="#666",
                            italic=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.all(10),
                        bgcolor=ft.Colors.with_opacity(0.1, "#6C63FF"),
                        border_radius=8,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#0f0c29", "#302b63", "#24243e"],
            ),
            padding=ft.padding.all(20),
        )
        
        self.pagina.add(contenedor_login)
        self.pagina.update()
    
    def mostrar_pantalla_registro(self):
        self.pagina.controls.clear()
        
        self.campo_reg_usuario = ft.TextField(
            label="Usuario (mínimo 3 caracteres)",
            width=320,
            autofocus=True,
            border_radius=12,
            filled=True,
            bgcolor="#1a1a2e",
            border_color="#FF6584",
            prefix_icon=ft.Icons.PERSON_ADD,
        )
        
        self.campo_reg_contrasena = ft.TextField(
            label="Contraseña (mínimo 4 caracteres)",
            width=320,
            password=True,
            can_reveal_password=True,
            border_radius=12,
            filled=True,
            bgcolor="#1a1a2e",
            border_color="#FF6584",
            prefix_icon=ft.Icons.LOCK,
        )
        
        self.campo_reg_confirmar = ft.TextField(
            label="Confirmar contraseña",
            width=320,
            password=True,
            can_reveal_password=True,
            on_submit=lambda _: self.registrar(),
            border_radius=12,
            filled=True,
            bgcolor="#1a1a2e",
            border_color="#FF6584",
            prefix_icon=ft.Icons.CHECK_CIRCLE,
        )
        
        self.mensaje_registro = ft.Text("", size=14)
        
        contenedor_registro = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=90, color="#FF6584"),
                    ft.Container(height=20),
                    ft.Text(
                        "Crear Cuenta Nueva",
                        size=38,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color="#FF6584",
                    ),
                    ft.Container(height=35),
                    self.campo_reg_usuario,
                    ft.Container(height=10),
                    self.campo_reg_contrasena,
                    ft.Container(height=10),
                    self.campo_reg_confirmar,
                    self.mensaje_registro,
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Registrarse",
                            width=320,
                            height=50,
                            on_click=lambda _: self.registrar(),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                bgcolor="#FF6584",
                                color="white",
                            ),
                        ),
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.Colors.with_opacity(0.3, "#FF6584"),
                            offset=ft.Offset(0, 4),
                        ),
                    ),
                    ft.Container(height=15),
                    ft.TextButton(
                        "¿Ya tienes cuenta? Inicia sesión",
                        on_click=lambda _: self.mostrar_pantalla_login(),
                        style=ft.ButtonStyle(color="#FF6584"),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#0f0c29", "#302b63", "#24243e"],
            ),
            padding=ft.padding.all(20),
        )
        
        self.pagina.add(contenedor_registro)
        self.pagina.update()
    
    def iniciar_sesion(self):
        nombre_usuario = self.campo_usuario.value
        contrasena = self.campo_contrasena.value
        
        exito, mensaje, usuario = auth.iniciar_sesion(nombre_usuario, contrasena)
        
        if exito:
            self.usuario_actual = usuario
            self.mensaje_login.value = ""
            self.mostrar_pantalla_chat()
        else:
            self.mensaje_login.value = mensaje
            self.mensaje_login.color = "#FF6584"
            self.pagina.update()
    
    def registrar(self):
        nombre_usuario = self.campo_reg_usuario.value
        contrasena = self.campo_reg_contrasena.value
        contrasena_confirmar = self.campo_reg_confirmar.value
        
        if contrasena != contrasena_confirmar:
            self.mensaje_registro.value = "Las contraseñas no coinciden"
            self.mensaje_registro.color = "#FF6584"
            self.pagina.update()
            return
        
        exito, mensaje, id_usuario = auth.registrar_usuario(nombre_usuario, contrasena)
        
        if exito:
            self.mensaje_registro.value = f"{mensaje}. Redirigiendo al login..."
            self.mensaje_registro.color = "#00FF88"
            self.pagina.update()
            
            import time
            time.sleep(1.5)
            self.mostrar_pantalla_login()
        else:
            self.mensaje_registro.value = mensaje
            self.mensaje_registro.color = "#FF6584"
            self.pagina.update()
    
    def mostrar_pantalla_chat(self):
        self.pagina.controls.clear()
        
        try:
            self.chatbot = ChatBotIA()
        except ValueError as e:
            dialogo_error = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error de Configuración"),
                content=ft.Text(str(e)),
                actions=[
                    ft.TextButton("OK", on_click=lambda _: self.pagina.close(dialogo_error))
                ],
            )
            self.pagina.overlay.append(dialogo_error)
            dialogo_error.open = True
            self.pagina.update()
            self.cerrar_sesion()
            return
        
        self.lista_chat = ft.ListView(
            expand=True,
            spacing=15,
            padding=20,
            auto_scroll=True,
        )
        
        self.cargar_historial_chat()
        
        self.campo_mensaje = ft.TextField(
            hint_text="Escribe tu mensaje aquí...",
            expand=True,
            multiline=True,
            max_lines=3,
            shift_enter=True,
            on_submit=lambda _: self.enviar_mensaje(),
            border_radius=25,
            filled=True,
            bgcolor="#1a1a2e",
            border_color="#6C63FF",
        )
        
        self.boton_enviar = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            tooltip="Enviar mensaje",
            on_click=lambda _: self.enviar_mensaje(),
            icon_color="#6C63FF",
            icon_size=28,
        )
        
        self.texto_estado = ft.Text("", size=12, italic=True, color="#8b8b8b")
        
        barra_superior = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=35, color="#6C63FF"),
                        bgcolor=ft.Colors.with_opacity(0.2, "#6C63FF"),
                        border_radius=50,
                        padding=8,
                    ),
                    ft.Text(
                        f"👤 {self.usuario_actual['username']}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.PEOPLE_OUTLINE,
                        tooltip="Gestionar Usuarios",
                        icon_color="#FFAB73",
                        on_click=lambda _: self.mostrar_gestion_usuarios(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_SWEEP_OUTLINED,
                        tooltip="Limpiar conversación",
                        icon_color="#FF6584",
                        on_click=lambda _: self.limpiar_conversacion(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT_ROUNDED,
                        tooltip="Cerrar sesión",
                        icon_color="#FF6584",
                        on_click=lambda _: self.cerrar_sesion(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#1a1a2e", "#16213e"],
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.3, "#000000"),
                offset=ft.Offset(0, 2),
            ),
        )
        
        area_entrada = ft.Container(
            content=ft.Column(
                [
                    self.texto_estado,
                    ft.Row(
                        [
                            self.campo_mensaje,
                            self.boton_enviar,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=8,
            ),
            padding=20,
            bgcolor="#16213e",
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.3, "#000000"),
                offset=ft.Offset(0, -2),
            ),
        )
        
        disposicion_principal = ft.Column(
            [
                barra_superior,
                ft.Container(
                    content=self.lista_chat,
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#0f0c29", "#1a1a2e"],
                    ),
                ),
                area_entrada,
            ],
            spacing=0,
            expand=True,
        )
        
        self.pagina.add(disposicion_principal)
        self.pagina.update()
    
    def mostrar_gestion_usuarios(self):
        usuarios = bd.obtener_todos_usuarios()
        
        lista_usuarios = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
        
        for usuario in usuarios:
            fecha = usuario['created_at'].split(' ')[0] if ' ' in usuario['created_at'] else usuario['created_at']
            
            tarjeta_usuario = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.PERSON, color="#6C63FF"),
                        ft.Column(
                            [
                                ft.Text(usuario['username'], weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"ID: {usuario['id']} | Creado: {fecha}", size=12, color="#8b8b8b"),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#FF6584",
                            tooltip="Eliminar usuario",
                            on_click=lambda e, uid=usuario['id'], uname=usuario['username']: self.confirmar_eliminar_usuario(uid, uname),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#1a1a2e",
                border_radius=12,
                border=ft.border.all(1, "#6C63FF"),
            )
            
            lista_usuarios.controls.append(tarjeta_usuario)
        
        def cerrar_dialogo(e):
            self.pagina.close(dialogo)
        
        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.PEOPLE, color="#6C63FF"),
                    ft.Text("Gestión de Usuarios", weight=ft.FontWeight.BOLD),
                ],
            ),
            content=ft.Container(
                content=lista_usuarios,
                width=500,
                height=400,
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=cerrar_dialogo,
                    style=ft.ButtonStyle(color="#6C63FF"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.pagina.overlay.append(dialogo)
        dialogo.open = True
        self.pagina.update()
    
    def confirmar_eliminar_usuario(self, id_usuario: int, nombre_usuario: str):
        def eliminar_usuario_confirmado(e):
            if bd.eliminar_usuario(id_usuario):
                self.pagina.close(dialogo_confirmacion)
                self.pagina.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Usuario '{nombre_usuario}' eliminado correctamente"),
                    bgcolor="#00FF88",
                )
                self.pagina.snack_bar.open = True
                self.pagina.update()
                
                for overlay in self.pagina.overlay:
                    if isinstance(overlay, ft.AlertDialog) and overlay.open:
                        self.pagina.close(overlay)
                
                self.mostrar_gestion_usuarios()
            else:
                self.pagina.close(dialogo_confirmacion)
                self.pagina.snack_bar = ft.SnackBar(
                    content=ft.Text("Error al eliminar usuario"),
                    bgcolor="#FF6584",
                )
                self.pagina.snack_bar.open = True
                self.pagina.update()
        
        def cancelar(e):
            self.pagina.close(dialogo_confirmacion)
        
        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar al usuario '{nombre_usuario}'?\nEsta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar, style=ft.ButtonStyle(color="#8b8b8b")),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=eliminar_usuario_confirmado,
                    style=ft.ButtonStyle(bgcolor="#FF6584", color="white"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.pagina.overlay.append(dialogo_confirmacion)
        dialogo_confirmacion.open = True
        self.pagina.update()
    
    def cargar_historial_chat(self):
        if not self.usuario_actual:
            return
        
        conversaciones = bd.obtener_conversaciones_usuario(self.usuario_actual['id'])
        
        for mensaje in conversaciones:
            self.agregar_mensaje_a_interfaz(mensaje['role'], mensaje['content'], guardar=False)
    
    def agregar_mensaje_a_interfaz(self, rol: str, contenido: str, guardar: bool = True):
        es_usuario = rol == 'user'
        
        contenedor_mensaje = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.PERSON if es_usuario else ft.Icons.SMART_TOY,
                                    size=20,
                                    color="white",
                                ),
                                bgcolor="#6C63FF" if es_usuario else "#00FF88",
                                border_radius=50,
                                padding=6,
                            ),
                            ft.Text(
                                "Tú" if es_usuario else "Asistente IA",
                                weight=ft.FontWeight.BOLD,
                                size=15,
                                color="white",
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(
                        content=ft.Text(contenido, selectable=True, color="white", size=14),
                        padding=15,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=["#6C63FF", "#5a54d6"] if es_usuario else ["#00C9A7", "#00B894"],
                        ) if es_usuario else None,
                        bgcolor=None if es_usuario else "#1a1a2e",
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.2, "#6C63FF" if es_usuario else "#00FF88"),
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                ],
                spacing=8,
            ),
            padding=ft.padding.only(left=20 if es_usuario else 0, right=0 if es_usuario else 20),
        )
        
        self.lista_chat.controls.append(contenedor_mensaje)
        self.pagina.update()
    
    def enviar_mensaje(self):
        mensaje = self.campo_mensaje.value.strip()
        
        if not mensaje:
            return
        
        self.campo_mensaje.value = ""
        self.campo_mensaje.focus()
        
        self.boton_enviar.disabled = True
        self.texto_estado.value = "📤 Enviando mensaje..."
        self.pagina.update()
        
        self.agregar_mensaje_a_interfaz('user', mensaje, guardar=False)
        
        self.texto_estado.value = "🤖 El asistente está escribiendo..."
        self.pagina.update()
        
        try:
            respuesta = self.chatbot.enviar_mensaje(self.usuario_actual['id'], mensaje)
            self.agregar_mensaje_a_interfaz('assistant', respuesta, guardar=False)
            self.texto_estado.value = ""
        except Exception as e:
            mensaje_error = f"Error: {str(e)}"
            self.agregar_mensaje_a_interfaz('assistant', mensaje_error, guardar=False)
            self.texto_estado.value = ""
        
        self.boton_enviar.disabled = False
        self.pagina.update()
    
    def limpiar_conversacion(self):
        def confirmar_limpiar(e):
            if e.control.text == "Sí":
                if self.chatbot:
                    self.chatbot.limpiar_historial(self.usuario_actual['id'])
                self.lista_chat.controls.clear()
                self.pagina.update()
            self.pagina.close(dialogo)
        
        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Confirmar"),
            content=ft.Text("¿Estás seguro de que deseas eliminar toda la conversación?"),
            actions=[
                ft.TextButton("No", on_click=lambda _: self.pagina.close(dialogo), style=ft.ButtonStyle(color="#8b8b8b")),
                ft.ElevatedButton("Sí", on_click=confirmar_limpiar, style=ft.ButtonStyle(bgcolor="#FF6584", color="white")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.pagina.overlay.append(dialogo)
        dialogo.open = True
        self.pagina.update()
    
    def cerrar_sesion(self):
        self.usuario_actual = None
        self.chatbot = None
        self.mostrar_pantalla_login()

def main(pagina: ft.Page):
    AplicacionChat(pagina)

if __name__ == "__main__":
    ft.app(target=main)
