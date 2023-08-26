#!/usr/bin/python3
'''Place module for the HBNB project'''
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    '''Amenity class'''
    from models.place import place_amenity
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary=place_amenity)