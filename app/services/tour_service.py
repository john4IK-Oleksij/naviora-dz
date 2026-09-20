from fastapi import HTTPException
from app.repositories.tour_repository import load_tours, save_tours
from app.models.tour import TourCreate, TourUpdate


class TourService:
    def get_all_tours(self):
        return load_tours()

    def search_tours(self, country: str | None = None):
        result = []
        for tour in load_tours():
            if tour["country"] == country:
                result.append(tour)
        return result

    def get_tour_by_id(self, tour_id: str):
        for tour in load_tours():
            if tour["id"] == tour_id:
                return tour
        else:
            raise HTTPException(status_code=404, detail="Tour not found")

    def create_tour(self, tour: TourCreate):
        tours_list = load_tours()
        tours_list.append(tour.model_dump())
        save_tours(tours_list)
        return tour

    def update_tour(self, tour_id: str, tour: TourUpdate):
        tours_list = load_tours()
        for item in tours_list:
            if item["id"] == tour_id:
                item.update(tour.model_dump(exclude_unset=True))
                save_tours(tours_list)
                return item
        else:
            raise HTTPException(status_code=404, detail="Tour not found")

    def delete_tour(self, tour_id: str):
        tours_list = load_tours()
        for item in tours_list:
            if item["id"] == tour_id:
                tours_list.remove(item)
                save_tours(tours_list)
                return item
        else:
            raise HTTPException(status_code=404, detail="Tour not found")

