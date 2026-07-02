from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from app.database import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = %s AND activo = TRUE",
        (email,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario or not bcrypt.checkpw(password.encode(), usuario["password_hash"].encode()):
        return templates.TemplateResponse(
            request, "login.html", {"error": "Correo o contraseña incorrectos"}
        )

    request.session["usuario"] = usuario["nombre"]
    request.session["usuario_id"] = usuario["id"]
    request.session["rol"] = usuario["rol"]

    return RedirectResponse(url="/productos", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")