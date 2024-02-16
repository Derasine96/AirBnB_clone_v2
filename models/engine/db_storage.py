#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """ClassDB is the base class for managing database storage."""
    __engine = None
    __session = None

    def __init__(self):
        """Create the SQLAlchemy engine."""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        connection_string = (
            "mysql+mysqldb://{}:{}@{}/{}"
            .format(user, passwd, host, db)
        )
        self.__engine = create_engine(connection_string, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """this method must return a dictionary: like FileStorage

        Args:
            cls (_type_, optional): class. Defaults to None.
        """
        result_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result_dict[key] = obj
        else:
            classes = [User, State, City, Amenity, Place, Review]
            for clas in classes:
                objects = self.__session.query(clas).all()
                for obj in objects:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
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
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()

    def close(self):
        """Close the current session."""
        self.__session.close()
