from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.api.routers.tours import router
from app.repositories.tour_repository import load_tours
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"name": "NAVIORA"}
    )

@app.get("/tours-page")
async def tours_page(request: Request):
    tours = load_tours()
    return templates.TemplateResponse(
        request=request,
        name="tours.html",
        context={"tours": tours}
    )






