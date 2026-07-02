# StockPro

Sistema web de gestión de inventario: control de productos, stock y reportes, desarrollado como proyecto demo.

## Tecnologías

- **Backend:** FastAPI + Uvicorn
- **Base de datos:** MySQL (mysql-connector-python)
- **Frontend:** Jinja2 + Bootstrap 5 (vía CDN)
- **Autenticación:** Sesiones con cookies (Starlette SessionMiddleware) + bcrypt

## Funcionalidades

- **Login** con sesiones y contraseñas hasheadas
- **Mantenimiento de productos**: crear, editar y desactivar (borrado lógico)
- **Control de stock**: registro de movimientos (entradas/salidas) con historial
- **Reportes**:
  - Stock bajo
  - Kardex de movimientos
  - Valorizado de inventario

## Estructura del proyecto

```
stockpro/
├── app/
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── database.py          # Conexión a MySQL
│   ├── dependencies.py      # Protección de rutas (requiere login)
│   ├── routers/
│   │   ├── auth.py
│   │   ├── productos.py
│   │   ├── stock.py
│   │   └── reportes.py
│   ├── templates/           # Vistas HTML (Jinja2)
│   └── static/               # CSS/JS propios
├── database.sql              # Script de creación de la base de datos
├── requirements.txt
├── .env.example
└── .gitignore
```

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/stockpro.git
cd stockpro
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
```

- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Linux/Mac:** `source venv/bin/activate`

Sabrás que está activo porque tu terminal muestra `(venv)` al inicio de la línea.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si necesitas reinstalar o actualizar todo:

```bash
pip install --upgrade -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y complétalo con tus datos:

```bash
cp .env.example .env       # Linux/Mac
copy .env.example .env     # Windows
```

Edita `.env` con tus credenciales de MySQL:

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=stockpro
SECRET_KEY=una_clave_secreta_larga_y_random
```

> El archivo `.env` **no se sube a GitHub** (está en `.gitignore`), ya que contiene credenciales sensibles.

### 5. Crear la base de datos

Ejecuta el script `database.sql` en MySQL Workbench (o el cliente que uses) para crear la base de datos `stockpro` y sus tablas (`usuarios`, `categorias`, `productos`, `movimientos_stock`).

### 6. Generar la contraseña del usuario administrador

El usuario de prueba se crea con una contraseña temporal (no hasheada). Genera el hash real así:

Crea un archivo temporal `generar_hash.py` en la raíz del proyecto:

```python
import bcrypt

password = "admin123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())
```

Ejecútalo:

```bash
python generar_hash.py
```

Copia el valor impreso (algo como `$2b$12$abcdefg...`) y actualiza el usuario en MySQL:

```sql
UPDATE usuarios
SET password_hash = 'PEGA_AQUI_EL_HASH_GENERADO'
WHERE email = 'admin@stockpro.com';
```

Una vez hecho esto, puedes borrar `generar_hash.py` — ya cumplió su función.

## Ejecutar el proyecto

Con el entorno virtual activo, desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

- `app.main:app` → busca la variable `app` dentro de `app/main.py`
- `--reload` → reinicia el servidor automáticamente al guardar cambios (útil en desarrollo)

Abre en el navegador:

```
http://127.0.0.1:8000/login
```

También puedes ver la documentación automática que genera FastAPI en:

```
http://127.0.0.1:8000/docs
```

## Credenciales de prueba

| Campo      | Valor                  |
|------------|-------------------------|
| Usuario    | admin@stockpro.com      |
| Contraseña | admin123                |

## Detener el proyecto

1. Detener el servidor: `Ctrl + C` en la terminal donde corre uvicorn
2. Desactivar el entorno virtual: `deactivate`
3. Detener MySQL (si usas XAMPP): desde el panel de control, botón *Stop* en el módulo MySQL

## Notas del diseño

- El **stock** no se edita directamente desde el formulario de productos: se actualiza únicamente mediante movimientos (entrada/salida) registrados en `movimientos_stock`, para mantener trazabilidad completa (kardex).
- Al "desactivar" un producto se hace **borrado lógico** (`activo = FALSE`), no se elimina de la base de datos. Los productos desactivados dejan de aparecer en listados y reportes.