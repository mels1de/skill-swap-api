from fastapi import FastAPI
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

app.include_router(auth.router, prefix="/auth", tags=["auth"])

def custom_openapi():
    print("custom_openapi called")

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

    for path in openapi_schema["paths"].values():
        for method in path.values():
            if method.get("operationId") != "login_auth_login_post":
               method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
