import os

from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    Request
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    HTMLResponse
)

from fastapi.staticfiles import (
    StaticFiles
)

from fastapi.templating import (
    Jinja2Templates
)

from .database import (
    Base,
    engine
)

from .routes.auth import (
    router as auth_router
)

from .routes.planners import (
    router as planner_router
)

from .routes.history import (
    router as history_router
)


load_dotenv()


@asynccontextmanager
async def lifespan(app):

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(

    title="PocketSmart AI",

    version="1.0.0",

    lifespan=lifespan
)


origins = [

    x.strip()

    for x in os.getenv(

        "ALLOWED_ORIGINS",

        "http://127.0.0.1:8000,http://localhost:8000"

    ).split(",")
]


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(BASE_DIR, "static")
    ),
    name="static"
)


    


app.mount(

    "/uploads",

    StaticFiles(
        directory="uploads"
    ),

    name="uploads"
)


templates = Jinja2Templates(

    directory="app/templates"
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def index(
    request: Request
):

    return templates.TemplateResponse(

        "index.html",

        {
            "request": request
        }
    )


PAGES = {

    "/login":
        "login.html",

    "/register":
        "register.html",

    "/dashboard":
        "dashboard.html",

    "/home-planner":
        "home.html",

    "/party-planner":
        "party.html",

    "/jewelry-planner":
        "jewelry.html",

    "/history":
        "history.html"
}


def create_page_handler(
    page
):

    def handler(
        request: Request
    ):

        return templates.TemplateResponse(

            page,

            {
                "request":
                    request
            }
        )

    return handler


for route, page in PAGES.items():

    app.add_api_route(

        route,

        create_page_handler(
            page
        ),

        response_class=HTMLResponse
    )


app.include_router(
    auth_router
)

app.include_router(
    planner_router
)

app.include_router(
    history_router
)

for route, page in PAGES.items():
    app.add_api_route(
        route,
        create_page_handler(page),
        response_class=HTMLResponse
    )

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.get("/startup")
def startup():

    return {
        "status": "ready"
    }


@app.get("/session-info")
def session_info():

    return {
        "message":
            "Use the login token for protected endpoints"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )