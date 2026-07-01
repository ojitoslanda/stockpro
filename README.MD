pip list
Deberías ver algo como fastapi, uvicorn, mysql-connector-python, Jinja2, python-multipart, itsdangerous, python-dotenv en la lista.


3. Levantar el servidor
Desde la raíz del proyecto (stockpro/, con el (venv) activo):
powershelluvicorn app.main:app --reload