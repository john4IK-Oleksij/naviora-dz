from fastapi import APIRouter

from app.models.tour import TourCreate, TourUpdate, TourOut
from app.services.tour_service import TourService
router = APIRouter()
service = TourService()

@router.get("/tours", response_model=list[TourOut])
async def get_tours():
    return service.get_all_tours()

@router.get("/tours/search", response_model=list[TourOut])
async def search_tours(country: str | None = None):
    return service.search_tours(country)

@router.get("/tours/{tour_id}", response_model=TourOut)
async def tours_item(tour_id: str):
    return service.get_tour_by_id(tour_id)

@router.post("/tours/", response_model=TourOut)
async def create_tour(tour: TourCreate):
    return service.create_tour(tour)

@router.put("/tours/{tour_id}", response_model=TourOut)
async def update_tour(tour_id: str, tour: TourUpdate):
    return service.update_tour(tour_id, tour)

@router.delete("/tours/{tour_id}", response_model=TourOut)
async def delete_tour(tour_id: str):
    return service.delete_tour(tour_id)