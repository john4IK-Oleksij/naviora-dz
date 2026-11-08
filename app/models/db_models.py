from sqlalchemy import Column, String, Integer, Float, JSON
from app.database import Base


class TourModel(Base):
    __tablename__ = "tours"

    id = Column(String(100), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False, index=True)
    durationDays = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    cities = Column(JSON, nullable=False)
    guide = Column(JSON, nullable=False)
    maxGuests = Column(Integer, nullable=True)
    image = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "country": self.country,
            "durationDays": self.durationDays,
            "price": self.price,
            "cities": self.cities,
            "guide": self.guide,
            "maxGuests": self.maxGuests,
            "image": self.image,
        }
