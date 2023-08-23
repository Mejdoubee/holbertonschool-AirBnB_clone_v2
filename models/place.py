#!/usr/bin/python3
"""Place module for the HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """Place class"""
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenities = relationship('Amenity', secondary=place_amenity, back_populates="place_amenities", viewonly=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = relationship('Amenity', secondary=place_amenity, back_populates="place_amenities", viewonly=False)
    else:
        @property
        def amenities(self):
            """Get amenities related to this place."""
            from models import storage
            all_amenities = storage.all(Amenity)
            return [amenity for amenity in all_amenities.values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Set amenities for this place."""
            if not isinstance(obj, Amenity):
                return
            if "amenity_ids" not in self.__dict__:
                self.amenity_ids = []
            self.amenity_ids.append(obj.id)
