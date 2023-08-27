#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    # Attributes
    name = Column(String(128), nullable=False)

    # Relationships & Properties
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        cities = relationship('City', cascade="all, delete-orphan", backref='state')
    else:
        @property
        def cities(self):
            """Get all City objects associated with this State."""
            from models import storage
            from models.city import City
            
            all_cities = storage.all(City)
            state_cities = [city for city in all_cities.values() if city.state_id == self.id]
            return state_cities
