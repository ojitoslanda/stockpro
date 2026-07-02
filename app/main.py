from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

from app.dependencies import NoAutenticado
from app.routers import auth, productos, stock, reportes

load_dotenv()

app = FastAPI(title="StockPro")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.exception_handler(NoAutenticado)
async def no_autenticado_handler(request, exc):
    return RedirectResponse(url="/login")


app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(stock.router)
app.include_router(reportes.router)