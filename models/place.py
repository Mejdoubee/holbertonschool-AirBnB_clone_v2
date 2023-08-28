#!/usr/bin/python3
"""Place Module for HBNB project"""
from os import getenv
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Table Definition
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """A place to stay"""
    __tablename__ = "places"

    # Attributes
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    # Relationships & Properties
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', cascade="all, delete, delete-orphan",
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 back_populates='place_amenities',
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """getter for reviews in filestorage use"""
            return [val for val in storage.all(Review).values()
                    if val.place_id == self.id]

        @property
        def amenities(self):
            """getter for amenity table. Returns Amenity instances for Place"""
            return [amenity for amenity in storage.all(Amenity).values()
                    if amenity.id == self.amenity_id]

        @amenities.setter
        def amenities(self, amenity_list):
            """Setter for amenities"""
            self.amenity_ids = [amenity for amenity in amenity_list
                                if isinstance(amenity, Amenity)]
