import reflex as rx # type: ignore
from Gestionproyectos.Component.navbar import render_navbar
from Gestionproyectos.Component.header import header
from Gestionproyectos.Component.footer import pie_de_pagina
from Gestionproyectos.views.usuario_vista import usuarios_page
from Gestionproyectos.views.proyecto_vista import proyectos_page
from Gestionproyectos.views.tarea_vista import tareas_page
from Gestionproyectos.views.colaboracion_vista import colaboraciones_page
from Gestionproyectos.views.avance_vista import avances_page
from Gestionproyectos.views.recurso_vista import recursos_page
from Gestionproyectos.views.planificacion_vista import planificaciones_page
from rxconfig import config

class State(rx.State):
    """The app state."""
    pass

def index() -> rx.Component:
    trabajos = [

        {
            'titulo': 'Gestión de proyectos',
            'descripcion': 'Proyecto de gestión de proyectos colaborativos',
            'image_url': 'iconos/proyectos.png'
        },
    ]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            render_navbar(),
            header(),
            lista_proyecto(trabajos),
            pie_de_pagina(),
        ),
        rx.logo(),
    )

def lista_proyecto(trabajos):
    return rx.hstack(*[
        rx.box(
            rx.image(src=trabajo['image_url']),
            rx.text(trabajo['titulo']),
            rx.text(trabajo['descripcion']),
            key=trabajo['titulo']
        ) for trabajo in trabajos
    ])


app = rx.App()
app.add_page(index, route="/")
app.add_page(usuarios_page, route="/usuarios")
app.add_page(proyectos_page, route="/proyectos")
app.add_page(tareas_page, route="/tareas")
app.add_page(colaboraciones_page, route="/colaboraciones")
app.add_page(avances_page, route="/avances")
app.add_page(recursos_page, route="/recursos")
app.add_page(planificaciones_page, route="/planificaciones")

