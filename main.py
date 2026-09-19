from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_naviora():
    return {"message": "Naviora API"}

from pydantic import BaseModel

class Tour(BaseModel):
    id :  str
    title: str
    country: str
    durationDays: int
    price: float
    maxGuests: int | None = None

tours_list = [
    {
        "id": "marrakech-fes-casablanca-journey",
        "title": "Marrakech, Fes & Casablanca Journey",
        "country": "morocco",
        "durationDays": 7,
        "price": 939,
        "maxGuests": 14
    },
    {
        "id": "alps-lakes-adventure",
        "title": "Alps & Lakes Adventure",
        "country": "switzerland",
        "durationDays": 5,
        "price": 749,
        "maxGuests": 12
    }
]
@app.get("/tours")
async def get_tours():
    return tours_list

@app.get("/tours/search")
async def search_tours(country: str | None = None):
    result = []
    for tour in tours_list:
        if tour["country"] == country:
            result.append(tour)
    return result

@app.get("/tours/{tour_id}")
async def tours_item(tour_id: str):
    for tour in tours_list:
        if tour["id"] == tour_id:
            return tour
    else:
        return {"error": "Tour not found"}

@app.post("/tours/")
async def create_tour(tour: Tour):
    tours_list.append(tour.model_dump())
    return tour

@app.put("/tours/{tour_id}")
async def update_tour(tour_id: str, tour: Tour):
    for item in tours_list:
        if item["id"] == tour_id:
            item.update(tour.model_dump())
            return item
    else:
        return {"error": "Tour not found"}






