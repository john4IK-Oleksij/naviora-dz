import json
import os
from app.database import engine, SessionLocal, Base
from app.models.db_models import TourModel

_db_initialized = False


def init_db():
    """Initializes tables and seeds initial tours from JSON if table is empty."""
    global _db_initialized
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(TourModel).first() is None:
            # Look for tours.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.normpath(os.path.join(current_dir, "../../data/tours.json"))
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as file:
                    tours_data = json.load(file)
                for item in tours_data:
                    tour = TourModel(
                        id=item["id"],
                        title=item["title"],
                        country=item["country"].strip().lower(),
                        durationDays=item["durationDays"],
                        price=item["price"],
                        cities=item["cities"],
                        guide=item["guide"],
                        maxGuests=item.get("maxGuests"),
                        image=item["image"],
                    )
                    db.add(tour)
                db.commit()
    except Exception as e:
        print(f"Warning during init_db: {e}")
    finally:
        db.close()
        _db_initialized = True


def ensure_initialized():
    global _db_initialized
    if not _db_initialized:
        init_db()


class TourRepository:
    def __init__(self):
        ensure_initialized()

    def get_all(self, country: str | None = None):
        db = SessionLocal()
        try:
            query = db.query(TourModel)
            if country:
                query = query.filter(TourModel.country == country.strip().lower())
            tours = query.all()
            return [t.to_dict() for t in tours]
        finally:
            db.close()

    def get_by_id(self, tour_id: str):
        db = SessionLocal()
        try:
            tour = db.query(TourModel).filter(TourModel.id == tour_id).first()
            return tour.to_dict() if tour else None
        finally:
            db.close()

    def create(self, tour_data: dict):
        db = SessionLocal()
        try:
            tour = TourModel(**tour_data)
            db.add(tour)
            db.commit()
            db.refresh(tour)
            return tour.to_dict()
        finally:
            db.close()

    def update(self, tour_id: str, update_data: dict):
        db = SessionLocal()
        try:
            tour = db.query(TourModel).filter(TourModel.id == tour_id).first()
            if not tour:
                return None
            for key, value in update_data.items():
                if value is not None:
                    setattr(tour, key, value)
            db.commit()
            db.refresh(tour)
            return tour.to_dict()
        finally:
            db.close()

    def delete(self, tour_id: str):
        db = SessionLocal()
        try:
            tour = db.query(TourModel).filter(TourModel.id == tour_id).first()
            if not tour:
                return None
            deleted_data = tour.to_dict()
            db.delete(tour)
            db.commit()
            return deleted_data
        finally:
            db.close()


repo = TourRepository()


def load_tours():
    """Backward compatibility helper."""
    return repo.get_all()
