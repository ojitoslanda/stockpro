pip list
Deberías ver algo como fastapi, uvicorn, mysql-connector-python, Jinja2, python-multipart, itsdangerous, python-dotenv en la lista.


3. Levantar el servidor
Desde la raíz del proyecto (stockpro/, con el (venv) activo):
uvicorn app.main:app --reload

4. Reinstalar  
pip install --upgrade -r requirements.txt

app.main:app → significa "adentro de la carpeta/archivo app/main.py, busca la variable app"
--reload → reinicia el servidor automáticamente cada vez que guardas un cambio (muy útil mientras desarrollas)


Y también puedes ver la documentación automática que genera FastAPI en:
http://127.0.0.1:8000/docs


1. Detener el servidor de FastAPI/uvicornEn la terminal donde está corriendo (donde ves los logs tipo INFO: Uvicorn running on...):Ctrl + C
Eso apaga el servidor. Verás que deja de escuchar peticiones.


2. Desactivar el entorno virtual
En la misma terminal (o cualquiera donde tengas (venv) activo):
deactivate




Ejecuta:
python generar_hash.py
Te va a imprimir algo como $2b$12$abcdefg.... Copia ese valor y actualízalo en MySQL Workbench:
UPDATE usuarios
SET password_hash = 'PEGA_AQUI_EL_HASH_GENERADO'
WHERE email = 'admin@stockpro.com';




Probar
Reinicia el servidor si hace falta:
uvicorn app.main:app --reload

http://127.0.0.1:8000/login