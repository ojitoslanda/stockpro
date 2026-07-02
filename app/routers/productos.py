from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import get_connection
from app.dependencies import requiere_login

router = APIRouter(prefix="/productos", dependencies=[Depends(requiere_login)])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def listar_productos(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.codigo, p.nombre, c.nombre AS categoria,
               p.precio, p.stock_actual, p.activo
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = TRUE
        ORDER BY p.nombre
    """)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse(request, "productos/listado.html", {"productos": productos})


@router.get("/nuevo")
def form_nuevo(request: Request):
    categorias = _obtener_categorias()
    return templates.TemplateResponse(
        request, "productos/formulario.html", {"categorias": categorias, "producto": None}
    )


@router.post("/nuevo")
def crear_producto(
    codigo: str = Form(...),
    nombre: str = Form(...),
    categoria_id: int = Form(...),
    precio: float = Form(...),
    stock_actual: int = Form(0),
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (codigo, nombre, categoria_id, precio, stock_actual) "
        "VALUES (%s, %s, %s, %s, %s)",
        (codigo, nombre, categoria_id, precio, stock_actual)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/productos", status_code=303)


@router.get("/{producto_id}/editar")
def form_editar(request: Request, producto_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    categorias = _obtener_categorias()
    return templates.TemplateResponse(
        request, "productos/formulario.html", {"categorias": categorias, "producto": producto}
    )


@router.post("/{producto_id}/editar")
def actualizar_producto(
    producto_id: int,
    codigo: str = Form(...),
    nombre: str = Form(...),
    categoria_id: int = Form(...),
    precio: float = Form(...),
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET codigo=%s, nombre=%s, categoria_id=%s, precio=%s WHERE id=%s",
        (codigo, nombre, categoria_id, precio, producto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/productos", status_code=303)


@router.post("/{producto_id}/eliminar")
def desactivar_producto(producto_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET activo = FALSE WHERE id = %s", (producto_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/productos", status_code=303)


def _obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return categorias