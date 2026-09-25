from pydantic import BaseModel, Field

class Guide(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    language: str = Field(min_length=2, max_length=30)

class TourBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    country: str = Field(min_length=2, max_length=50)
    guide: Guide
    durationDays: int = Field(gt=0)
    price: float = Field(gt=0)
    cities: list[str] = Field(min_length=1)
    image: str = Field(min_length=1, max_length=255)
    maxGuests: int | None = Field(default=None, gt=0)

class TourCreate(TourBase):
    id: str = Field(min_length=2, max_length=100)

class TourUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    country: str | None = Field(default=None, min_length=2, max_length=50)
    guide: Guide | None = None
    durationDays: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)
    cities: list[str] | None = Field(default=None, min_length=1)
    image: str | None = Field(default=None, min_length=1, max_length=255)
    maxGuests: int | None = Field(default=None, gt=0)

class TourOut(TourBase):
    id: str