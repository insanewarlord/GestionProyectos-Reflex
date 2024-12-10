import reflex as rx
from ..styles.color import Color
from .link_icon import link_icon

def render_navbar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.image(
                src="favicon.ico",
                width=100,
                height=100,
                border_radius="15px 50px",
                border="5px solid #555"
            ),
            rx.text(
                "Sistema de Gestión de Proyectos",
                font_size="2em",
                padding_y="0.75em",
                padding_x="0.2em",
            ),
            rx.spacer(),
            rx.menu.root(
                rx.menu.trigger(
                    rx.button("Menu"),
                ),
                rx.menu.content(
                    rx.menu.item("Inicio", on_click=lambda: rx.redirect
                    ("/")),
                    rx.menu.separator(),
                    rx.menu.item("Usuarios", on_click=lambda: rx.redirect
                    ("/usuarios")),
                    rx.menu.item("Proyectos", on_click=lambda: rx.redirect
                    ("/proyectos")),
                    rx.menu.item("Planificacion", on_click=lambda: rx.redirect
                    ("/planificaciones")),
                    rx.menu.item("Avance", on_click=lambda: rx.redirect
                    ("/avances")),
                    rx.menu.item("Colaboración", on_click=lambda: rx.redirect
                    ("/colaboraciones"))
                ),
            ),
        ),
        background_color=Color.BACKGROUND.value,
        position="sticky",
        border_bottom=f"0.25 solid {Color.SECONDARY.value}",
        padding="10px",
        z_index="999",
        top="0",
        width="100%",
    )
