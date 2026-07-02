from fastapi import Request


class NoAutenticado(Exception):
    """Se lanza cuando no hay sesión activa."""
    pass


def requiere_login(request: Request):
    if not request.session.get("usuario_id"):
        raise NoAutenticado()
    return {
        "id": request.session.get("usuario_id"),
        "nombre": request.session.get("usuario"),
        "rol": request.session.get("rol"),
    }