#!/usr/bin/python3
"""
DBStorage module
"""
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import os


class DBStorage:
    """
    DBStorage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialization of DBStorage class
        """
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        database = os.environ.get('HBNB_MYSQL_DB')
        engine_url = 'mysql+mysqldb://{}:{}@{}/{}'.format(user, password,
                                                          host, database)
        self.__engine = create_engine(engine_url, pool_pre_ping=True)

        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        Session = orm.sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """
        Returns all instances of the class
        """
        objects = []
        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                objects.extend(self.__session.query(cls).all())

        result = {}
        for obj in objects:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            result[key] = obj
        return result

    def new(self, obj):
        """
        Adds a new object to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits changes to the session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads all tables
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """
        Closes or removes the current session
        """
        if self.__session:
            self.__session.remove()
