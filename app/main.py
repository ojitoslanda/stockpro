from fastapi import FastAPI
from app.database import get_connection

app = FastAPI(title="StockPro")

@app.get("/")
def home():
    return {"mensaje": "StockPro funcionando 🚀"}

@app.get("/test-db")
def test_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"productos_en_bd": total}