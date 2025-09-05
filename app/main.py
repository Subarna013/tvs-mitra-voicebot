# app/main.py
from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.openapi.utils import get_openapi
import os
import logging
from dotenv import load_dotenv
from app.routers import customer, payment  # ✅ import payment router

# ----------------- Load environment variables -----------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_API_KEY = os.getenv("API_KEY")

# ----------------- Logging -----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------- Security -----------------
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials.")


# ----------------- FastAPI instance -----------------
app = FastAPI(
    title="TVS Mitra Agentic Core API",
    version="1.0.0"
)

# ----------------- Routers -----------------
app.include_router(customer.router, dependencies=[Depends(get_api_key)])
app.include_router(payment.router, dependencies=[Depends(get_api_key)])  # ✅ add payment

# ----------------- Public endpoint -----------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"message": "Hello from TVS Mitra!"}

# ----------------- Custom OpenAPI with API key -----------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="TVS Mitra API with API Key Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": API_KEY_NAME,
        }
    }
    openapi_schema["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# app/main.py
from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.openapi.utils import get_openapi
import os
import logging
from dotenv import load_dotenv
from app.routers import customer, payment  # ✅ import payment router

# ----------------- Load environment variables -----------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_API_KEY = os.getenv("API_KEY")

# ----------------- Logging -----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------- Security -----------------
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials.")


# ----------------- FastAPI instance -----------------
app = FastAPI(
    title="TVS Mitra Agentic Core API",
    version="1.0.0"
)

# ----------------- Routers -----------------
app.include_router(customer.router, dependencies=[Depends(get_api_key)])
app.include_router(payment.router, dependencies=[Depends(get_api_key)])  # ✅ add payment

# ----------------- Public endpoint -----------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"message": "Hello from TVS Mitra!"}

# ----------------- Custom OpenAPI with API key -----------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="TVS Mitra API with API Key Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": API_KEY_NAME,
        }
    }
    openapi_schema["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
