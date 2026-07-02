from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.database import get_connection
from app.dependencies import requiere_login

router = APIRouter(prefix="/reportes", dependencies=[Depends(requiere_login)])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def menu_reportes(request: Request):
    return templates.TemplateResponse(request, "reportes/menu.html")


@router.get("/stock-bajo")
def reporte_stock_bajo(request: Request, umbral: int = 5):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.codigo, p.nombre, c.nombre AS categoria, p.stock_actual
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = TRUE AND p.stock_actual <= %s
        ORDER BY p.stock_actual ASC
    """, (umbral,))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse(
        request, "reportes/stock_bajo.html", {"productos": productos, "umbral": umbral}
    )


@router.get("/kardex")
def reporte_kardex(request: Request, producto_id: int = None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT m.fecha, p.codigo, p.nombre AS producto, m.tipo, m.cantidad,
               m.motivo, u.nombre AS usuario
        FROM movimientos_stock m
        JOIN productos p ON m.producto_id = p.id
        LEFT JOIN usuarios u ON m.usuario_id = u.id
    """
    params = ()
    if producto_id:
        query += " WHERE m.producto_id = %s"
        params = (producto_id,)
    query += " ORDER BY m.fecha DESC"

    cursor.execute(query, params)
    movimientos = cursor.fetchall()

    cursor.execute("SELECT id, codigo, nombre FROM productos ORDER BY nombre")
    productos = cursor.fetchall()

    cursor.close()
    conn.close()
    return templates.TemplateResponse(
        request, "reportes/kardex.html",
        {"movimientos": movimientos, "productos": productos, "producto_id": producto_id}
    )


@router.get("/valorizado")
def reporte_valorizado(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.nombre AS categoria,
               SUM(p.stock_actual) AS total_unidades,
               SUM(p.stock_actual * p.precio) AS valor_total
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = TRUE
        GROUP BY c.nombre
        ORDER BY valor_total DESC
    """)
    por_categoria = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(stock_actual * precio) AS total
        FROM productos WHERE activo = TRUE
    """)
    total_general = cursor.fetchone()["total"] or 0

    cursor.close()
    conn.close()
    return templates.TemplateResponse(
        request, "reportes/valorizado.html",
        {"por_categoria": por_categoria, "total_general": total_general}
    )