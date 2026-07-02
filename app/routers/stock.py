from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import get_connection
from app.dependencies import requiere_login

router = APIRouter(prefix="/stock", dependencies=[Depends(requiere_login)])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def listar_stock(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.codigo, p.nombre, c.nombre AS categoria, p.stock_actual
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = TRUE
        ORDER BY p.nombre
    """)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse(request, "stock/listado.html", {"productos": productos})


@router.get("/movimiento")
def form_movimiento(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, codigo, nombre, stock_actual FROM productos WHERE activo = TRUE ORDER BY nombre")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse(request, "stock/movimiento.html", {"productos": productos})


@router.post("/movimiento")
def registrar_movimiento(
    request: Request,
    producto_id: int = Form(...),
    tipo: str = Form(...),
    cantidad: int = Form(...),
    motivo: str = Form(""),
):
    usuario_id = request.session.get("usuario_id")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Validar stock suficiente si es salida
    if tipo == "salida":
        cursor.execute("SELECT stock_actual FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        if not producto or producto["stock_actual"] < cantidad:
            cursor.close()
            conn.close()
            # Volvemos a cargar el formulario con un mensaje de error
            conn2 = get_connection()
            cursor2 = conn2.cursor(dictionary=True)
            cursor2.execute("SELECT id, codigo, nombre, stock_actual FROM productos WHERE activo = TRUE ORDER BY nombre")
            productos = cursor2.fetchall()
            cursor2.close()
            conn2.close()
            return templates.TemplateResponse(
                request, "stock/movimiento.html",
                {"productos": productos, "error": "Stock insuficiente para esta salida"}
            )

    # Registrar el movimiento
    cursor.execute(
        "INSERT INTO movimientos_stock (producto_id, tipo, cantidad, motivo, usuario_id) "
        "VALUES (%s, %s, %s, %s, %s)",
        (producto_id, tipo, cantidad, motivo, usuario_id)
    )

    # Actualizar stock_actual del producto
    if tipo == "entrada":
        cursor.execute(
            "UPDATE productos SET stock_actual = stock_actual + %s WHERE id = %s",
            (cantidad, producto_id)
        )
    else:
        cursor.execute(
            "UPDATE productos SET stock_actual = stock_actual - %s WHERE id = %s",
            (cantidad, producto_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/stock", status_code=303)