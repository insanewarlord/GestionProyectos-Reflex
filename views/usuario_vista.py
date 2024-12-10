import reflex as rx # type: ignore
from Gestionproyectos.models.models import Usuario
from Gestionproyectos.servicios.usuario_servicio import (
    servicio_usuarios_all,
    servicio_consultar_usuario_id,
    servicio_crear_usuario,
    servicio_eliminar_usuario,
    servicio_actualizar_usuario,
    servicio_editar_usuario
    
    
)

class UsuarioState(rx.State):
    usuarios: list[Usuario] = []
    buscar_id: int = 0
    usuario_a_editar: Usuario | None = None

    @rx.background
    async def get_todos_usuarios(self):
        async with self:
            self.usuarios = servicio_usuarios_all()
            

    @rx.background
    async def get_usuario_id(self):
        async with self:
            self.usuarios = servicio_consultar_usuario_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        try:
          self.buscar_id = int(value) if value.strip() else 0
        except ValueError:
          print("Error: ID de usuario inválido")

        
    @rx.background
    async def iniciar_editar_usuario(self, usuario: Usuario):
        async with self:
         self.usuario_a_editar = usuario
        


    @rx.background
    async def crear_usuario(self, data: dict):
        async with self:
            try:
                # Extrae los valores del formulario
                id = int(data.get('id'))
                nombre = data.get('nombre')
                email = data.get('email')
                tipo = data.get('tipo')
                print(f'Crear usuario con id={id}, nombre={nombre}, email={email}, tipo={tipo}')
                # Llama al servicio con los valores extraídos
                resultado = servicio_crear_usuario(id, nombre, email, tipo)
                if resultado == "El usuario ya existe":
                    print(resultado)
                else:
                    self.usuarios.append(resultado)
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_usuario(self, id: int):
        async with self:
            try:
                servicio_eliminar_usuario(id)
                yield UsuarioState.get_todos_usuarios()
            except Exception as e:
                print(e)
                
    @rx.background
    async def editar_usuario(self, data):
      async with self:
        try:
            print(f"Datos recibidos para editar: {data}")  # Verifica los datos recibidos

            # Extrae los valores
            id = data.get("id")
            nombre = data.get("nombre")
            email = data.get("email")
            tipo = data.get("tipo")

            # Validación de datos
            if not all([id, nombre, email, tipo]):
                raise ValueError("Todos los campos son obligatorios")

            # Convierte ID a entero
            id = int(id)

            # Llama al servicio para actualizar
            resultado = servicio_actualizar_usuario(id, nombre, email, tipo)
            if resultado == "El usuario no existe":
                print("Error: El usuario no existe")
            else:
                # Actualiza la lista local
                for i, usuario in enumerate(self.usuarios):
                    if usuario.id == id:
                        self.usuarios[i] = resultado
                        print("Usuario editado con éxito")
                        break

        except ValueError as e:
            print(f"Error al editar usuario: {e}")
        except Exception as e:
            print(f"Error inesperado al editar usuario: {e}")


    





@rx.page(route="/usuarios", title="Lista de Usuarios", on_load=UsuarioState.get_todos_usuarios)
def usuarios_page() -> rx.Component:
    return rx.flex(
        rx.heading("Usuarios", title="Usuarios", size="5", center=True),
        rx.vstack(
            buscar_usuario_id(),
            dialog_usuario_form(),
            rx.cond(
                UsuarioState.usuario_a_editar,  # Mostrar el diálogo solo si hay un usuario a editar
                dialog_editar_usuario(UsuarioState.usuario_a_editar),
            ),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
            
        ),
        tabla_usuarios(UsuarioState.usuarios),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_usuarios(lista_usuarios: list[Usuario]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Tipo"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_usuarios, row_table_usuario)
        ),
    )

def row_table_usuario(usuario: Usuario) -> rx.Component:
    return rx.table.row(
        rx.table.cell(usuario.id),
        rx.table.cell(usuario.nombre),
        rx.table.cell(usuario.email),
        rx.table.cell(usuario.tipo),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: UsuarioState.eliminar_usuario(usuario.id)),
                rx.button("Editar", on_click=lambda: UsuarioState.iniciar_editar_usuario(usuario)),
            )
        ),
    )

def buscar_usuario_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Usuario", on_change=UsuarioState.buscar_onchange),
        rx.button("Buscar Usuario", on_click=UsuarioState.get_usuario_id)
    )

def dialog_usuario_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Usuario", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Usuario"),
                crear_usuario_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="red"),
                ),
                spacing="2",
                justify="end",
                margin_top="10px",
            ),
            style={"width": "400px"},
        ),
    )

def dialog_editar_usuario(usuario: Usuario) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Editar Usuario", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Editar Usuario"),
                form_editar_usuario(usuario),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="red"),
                ),
                spacing="2",
                justify="end",
                margin_top="10px",
            ),
            style={"width": "400px"},
        ),
        is_open=True,  # Asegura que se abra al activarlo
    )

def crear_usuario_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Email", name="email"),
            rx.input(placeholder="Tipo", name="tipo"),
            rx.dialog.close(
                rx.button("Crear Usuario", type="submit"),
            ),
        ),
        on_submit=UsuarioState.crear_usuario,
    )
    
    
    
def form_editar_usuario(usuario: Usuario) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                value=rx.cond(usuario.id, str(usuario.id), ""), 
                name="id", disabled=True, style={"width": "100px"}
            ),
            rx.input(
                value=rx.cond(usuario.nombre, usuario.nombre, ""), 
                name="nombre", placeholder="Nombre", required=True
            ),
            rx.input(
                value=rx.cond(usuario.email, usuario.email, ""), 
                name="email", placeholder="Email", required=True
            ),
            rx.input(
                value=rx.cond(usuario.tipo, usuario.tipo, ""), 
                name="tipo", placeholder="Tipo", required=True
            ),
            rx.dialog.close(
                rx.button("Guardar Cambios", type="submit"),
            ),
        ),
        on_submit=UsuarioState.editar_usuario,
    )






  

    