from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routers.tours import router
from app.repositories.tour_repository import init_db
from app.services.tour_service import TourService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and seed initial data if empty
    init_db()
    yield


app = FastAPI(title="NAVIORA Tours", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

templates = Jinja2Templates(directory="templates")
tour_service = TourService()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"name": "NAVIORA"}
    )


@app.get("/tours-page")
async def tours_page(request: Request):
    tours = tour_service.get_all_tours()
    return templates.TemplateResponse(
        request=request,
        name="tours.html",
        context={
            "tours": tours,
            "is_admin": False
        }
    )
