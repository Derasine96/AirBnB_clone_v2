#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base import Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'  # Corrected typo
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
        return [obj for obj in self.__objects.values()
                if isinstance(obj, City) and obj.state_id == self.id]
