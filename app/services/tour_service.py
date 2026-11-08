from fastapi import HTTPException
from app.repositories.tour_repository import TourRepository
from app.models.tour import TourCreate, TourUpdate


class TourService:
    def __init__(self):
        self.repo = TourRepository()

    def get_all_tours(self):
        return self.repo.get_all()

    def search_tours(self, country: str | None = None):
        return self.repo.get_all(country=country)

    def get_tour_by_id(self, tour_id: str):
        tour = self.repo.get_by_id(tour_id)
        if not tour:
            raise HTTPException(status_code=404, detail="Tour not found")
        return tour

    def create_tour(self, tour: TourCreate):
        existing = self.repo.get_by_id(tour.id)
        if existing:
            raise HTTPException(status_code=400, detail="Tour with this ID already exists")
        return self.repo.create(tour.model_dump())

    def update_tour(self, tour_id: str, tour: TourUpdate):
        updated = self.repo.update(tour_id, tour.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Tour not found")
        return updated

    def delete_tour(self, tour_id: str):
        deleted = self.repo.delete(tour_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Tour not found")
        return deleted
