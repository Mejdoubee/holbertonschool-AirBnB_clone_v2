#!/usr/bin/python3
'''
State Module for HBNB project'''
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    '''State class'''
    storageType = getenv("HBNB_TYPE_STORAGE")
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if storageType == 'db':
        cities = relationship('City',
                              cascade="all, delete-orphan",
                              backref='state'
                              )

    else:
        @property
        def cities(self):
            '''Get all City objects associated with this State'''
            from models import storage

            citiess = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    citiess.append(value)
            return citiess
