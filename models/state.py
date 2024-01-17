#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    # For DBStorage
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')

    # For FileStorage
    @property
    def get_cities(self):
        """Getter attribute that returns a list of City instances
            with state_id equal to the current State.id
        """
        return [city for city in self.places if city.state_id == self.id]
