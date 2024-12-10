import reflex as rx 

def header() -> rx.Component:
    return rx.grid(
        rx.center(
            rx.box(
                rx.heading("Sistema de Gestión de Proyectos", size="4"),
                rx.heading("Empresa Ficticia :)", size="3"),
            )
        ),
        rx.center(
            rx.image( 
                src="hospital.png",
                width="200px",
                height="auto",
                )
        ),
        columns="2",
        spacing="2",
        width="100%",
    )