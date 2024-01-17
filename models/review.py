#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    text = Column(String(1024), nullable=False)

    # For FileStorage
    @property
    def get_reviews(self):
        """Getter attribute that returns a list of City instances
                with state_id equal to the current State.id
        """
        return [obj for obj in self.__objects.values()
                if isinstance(obj, Review) and obj.place_id == self.id]
