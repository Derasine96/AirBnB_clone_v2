#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ClassDB is the base class for managing database storage."""
    __engine = None
    __session = None

    def __init__(self):
        """Instatntiates a new engine"""
        self.create_engine()

    def create_engine(self):
        """Create the SQLAlchemy engine."""
        from models.base_model import BaseModel
        user = os.environ.get('HBNB_MYSQL_USER', 'default_user')
        password = os.environ.get('HBNB_MYSQL_PWD', 'default_password')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB', 'default_database')
        connection_string = f'mysql+mysqldb://'
        '{user}:{password}@{host}/{database}'
        if os.environ.get('HBNB_ENV') == 'test':
            metadata = MetaData(bind=create_engine
                                (connection_string, pool_pre_ping=True))
            metadata.reflect()
            metadata.drop_all()
        self.__engine = create_engine(connection_string, pool_pre_ping=True)

    def all(self, cls=None):
        """this method must return a dictionary: like FileStorage

        Args:
            cls (_type_, optional): class. Defaults to None.
        """
        classes = [User, State, City, Amenity, Place, Review]
        if cls is not None:
            classes = [cls]
        result_dict = {}
        for cls in classes:
            objects = self.__session.query(cls).all()
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

    def reload(self):
        """Create all tables in the database"""
        from models.base_model import Base
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
        Base.metadata.create_all(self.__engine)
