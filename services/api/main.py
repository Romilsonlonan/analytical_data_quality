from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Industrial Logistics Platform API",
    description="API para acesso aos dados da plataforma",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "Industrial Logistics Platform",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/v1/orders")
def get_orders():
    """Retorna pedidos do Data Warehouse"""
    return {"orders": [], "count": 0}


@app.get("/api/v1/deliveries")
def get_deliveries():
    """Retorna entregas do Data Warehouse"""
    return {"deliveries": [], "count": 0}


@app.get("/api/v1/metrics")
def get_metrics():
    """Retorna métricas agregadas"""
    return {"metrics": {}}
