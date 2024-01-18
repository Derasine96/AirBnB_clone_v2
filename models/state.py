#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    # For DBStorage
    cities = relationship('City', backref='state',
                          cascade='all, delete, delete-orphan')

    # For FileStorage
    @property
    def cities(self):
        """Getter attribute that returns a list of City instances
            with state_id equal to the current State.id
        """
        city_list = []
        for city in list(models.storage.all(City).values()):
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
