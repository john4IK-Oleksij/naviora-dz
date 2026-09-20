from pydantic import BaseModel

class Guide(BaseModel):
    name: str
    language: str

class TourBase(BaseModel):
    title: str
    country: str
    guide: Guide
    durationDays: int
    price: float
    cities: list[str]
    maxGuests: int | None = None

class TourCreate(TourBase):
    id: str

class TourUpdate(BaseModel):
    title: str | None = None
    country: str | None = None
    guide: Guide | None = None
    durationDays: int | None = None
    price: float | None = None
    cities: list[str] | None = None
    maxGuests: int | None = None

class TourOut(TourBase):
    id: str