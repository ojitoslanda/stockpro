from fastapi import FastAPI

app = FastAPI(title="StockPro")

@app.get("/")
def home():
    return {"mensaje": "StockPro funcionando 🚀"}