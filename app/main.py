from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api import auth
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="SkillSwap API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API for SkillSwap",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    if "/auth/me" in openapi_schema["paths"]:
        openapi_schema["paths"]["/auth/me"]["get"] = {
            **openapi_schema["paths"]["/auth/me"]["get"],
            "security": [{"BearerAuth": []}]
        }

    for path_name, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if path_name != "/auth/login" and method.lower() != "options":
                operation.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi