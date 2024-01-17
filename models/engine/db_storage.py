#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


Base = declarative_base()


class DBStorage:
    """ClassDB is the base class for managing database storage."""
    __engine = None
    __session = None

    def __init__(self):
        """Instatntiates a new engine"""
        self.__engine = self.create_engine()

    def create_engine(self):
        """Create the SQLAlchemy engine."""
        from models.base_model import BaseModel
        user = os.environ.get('HBNB_MYSQL_USER', 'hbnb_dev')
        password = os.environ.get('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB', 'hbnb_dev_db')
        connection_string = f'mysql+mysqldb://'
        '{user}:{password}@{host}/{database}'
        engine = create_engine(connection_string, pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(engine)
        return engine

    def all(self, cls=None):
        """this method must return a dictionary: like FileStorage

        Args:
            cls (_type_, optional): class. Defaults to None.
        """
        classes = [User, State, City, Amenity, Place, Review]
        if cls is not None:
            classes = [cls]
        result_dict = {}
        for clas in classes:
            objects = self.__session.query(clas).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result_dict[key] = obj
        return result_dict

    def new(self, obj):
        """add the object to the current database session
        Args:
            obj: object to be added
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
        Base.metadata.create_all(self.__engine)
