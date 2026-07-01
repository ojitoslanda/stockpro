pip list
Deberías ver algo como fastapi, uvicorn, mysql-connector-python, Jinja2, python-multipart, itsdangerous, python-dotenv en la lista.


3. Levantar el servidor
Desde la raíz del proyecto (stockpro/, con el (venv) activo):
uvicorn app.main:app --reload


app.main:app → significa "adentro de la carpeta/archivo app/main.py, busca la variable app"
--reload → reinicia el servidor automáticamente cada vez que guardas un cambio (muy útil mientras desarrollas)


Y también puedes ver la documentación automática que genera FastAPI en:
http://127.0.0.1:8000/docs


1. Detener el servidor de FastAPI/uvicornEn la terminal donde está corriendo (donde ves los logs tipo INFO: Uvicorn running on...):Ctrl + C
Eso apaga el servidor. Verás que deja de escuchar peticiones.


2. Desactivar el entorno virtual
En la misma terminal (o cualquiera donde tengas (venv) activo):
deactivate