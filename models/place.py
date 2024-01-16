#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.orm import relationship


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey(cities.id), nullable=False)
    user_id = Column(String(60), ForeignKey(users.id), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nulable=False, default=0)
    number_bathrooms = Column(Integer, nulable=False, default=0)
    max_guest = Column(Integer, nulable=False, default=0)
    price_by_night = Column(Integer, nulable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []
    reviews = relationship('Review', backref='place',
                           cascade='all, delete-orphan')

    # For FileStorage
    @property
    def get_reviws(self):
        """Getter attribute that returns a list of City instances
                with state_id equal to the current State.id
        """
        return [obj for obj in self.__objects.values()
                if isinstance(obj, Review) and obj.place_id == self.id]
