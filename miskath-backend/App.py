# App.py
"""
Archivo principal: crea e inicia la aplicación FastAPI, según el patrón
del PDF (App.py se encarga de crear e iniciar la app).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from Config import appTitle, appDescription, appVersion, corsOrigins, limiter
from Bootstrap import runBootstrap

from Routes.AuthRoutes import AuthRoutes
from Routes.ProductRoutes import ProductRoutes
from Routes.BrandRoutes import BrandRoutes
from Routes.CategoryRoutes import CategoryRoutes
from Routes.TypeRoutes import TypeRoutes
from Routes.UserRoutes import UserRoutes
from Routes.CartRoutes import CartRoutes
from Routes.OrderRoutes import OrderRoutes
from Routes.PaymentRoutes import PaymentRoutes

app = FastAPI(
    title=appTitle,
    description=appDescription,
    version=appVersion,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
def startupBootstrap():
    runBootstrap()


app.add_middleware(
    CORSMiddleware,
    allow_origins=corsOrigins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRoutes)
app.include_router(ProductRoutes)
app.include_router(BrandRoutes)
app.include_router(UserRoutes)
app.include_router(CartRoutes)
app.include_router(OrderRoutes)
app.include_router(PaymentRoutes)
app.include_router(CategoryRoutes)
app.include_router(TypeRoutes)


@app.get("/health", tags=["Health"])
def healthCheck():
    # Endpoint simple para verificar que la API está viva.
    return {"status": "ok"}
