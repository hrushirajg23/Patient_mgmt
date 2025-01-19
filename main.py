from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_events.handlers.local import local_handler
from starlette.middleware.sessions import SessionMiddleware
from fastapi_pagination import add_pagination
from config import setting

origins = ["http://localhost", "http://localhost:3000/", ""]


description = """
Patient Management System by Hrushiraj Gandhi.
"""
app = FastAPI(
    title="Hrushiraj Gandhi",
    docs_url="/",
    redoc_url=None,
    description=description,
    version="0.0.1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

add_pagination(app)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hrushiraj Gandhi",
        version="0.1.0",
        description="Hrushiraj Gandhi's API",
        routes=app.routes,
        servers=[{"url": setting.SERVER}] if setting.SERVER != "" else [],
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema



app.openapi = custom_openapi

# System middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.add_middleware(SessionMiddleware, secret_key=setting.secret_key)
# app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])
# app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def home():
    return {"message": "Contact to Map My Crop Admin for more details"}

