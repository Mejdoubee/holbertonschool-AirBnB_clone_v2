#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import uuid


class State(BaseModel, Base):
    '''
    Inherits from BaseModel and Base
    '''
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def cities(self):
        from models import storage
        all_cities = storage.all(City)
        return [city for city in all_cities.values()
                if city.state_id == self.id]
