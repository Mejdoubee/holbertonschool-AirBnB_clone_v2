#!/usr/bin/python3
'''
Model that defines BaseModel class
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, ForeignKey
import uuid
from datetime import datetime


Base = declarative_base()


class BaseModel:
    '''
    This class defines all common attributes/methods for other classes
    '''
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        '''
        Initialization of the base model
        '''
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        '''
        Returns a string representation of the instance.
        '''
        dict_repr = self.to_dict().copy()

        # Use the datetime module directly for formatting
        dict_repr["created_at"] = datetime.strftime(
            self.created_at, "datetime.datetime(%Y, %m, %d, %H, %M, %S)")
        dict_repr["updated_at"] = datetime.strftime(
            self.updated_at, "datetime.datetime(%Y, %m, %d, %H, %M, %S)")

        if '__class__' in dict_repr:
            del dict_repr['__class__']

        # Constructing the string representation manually
        attr_str = ", ".join(
            ["'{}': {}".format(k, v) for k, v in dict_repr.items()])
        return "[{}] ({}) {{{}}}".format(
            self.__class__.__name__, self.id, attr_str)

    def save(self):
        '''
        Updates the public instance attribute
        "updated_at" with the current datetime
        '''
        self.updated_at = datetime.now()
        from . import storage
        storage.new(self)
        storage.save()

    def delete(self):
        '''
        Deletes the current instance from the storage
        '''
        from . import storage
        storage.delete(self)
        storage.save()

    def to_dict(self):
        '''
        Return a dictionary containing all
        keys/values of __dict__ of the instance
        '''
        dict_copy = self.__dict__.copy()
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in dict_copy:
            del (dict_copy['_sa_instance_state'])
        return dict_copy
    def to_dict(self):
        '''Return dictionary representation of instance.'''
        dict_copy = self.__dict__.copy()

        if "created_at" in dict_copy and isinstance(dict_copy["created_at"], datetime):
            dict_copy["created_at"] = dict_copy["created_at"].isoformat()
        if "updated_at" in dict_copy and isinstance(dict_copy["updated_at"], datetime):
            dict_copy["updated_at"] = dict_copy["updated_at"].isoformat()
        dict_copy["__class__"] = self.__class__.__name__
        if '_sa_instance_state' in dict_copy:
                del (dict_copy['_sa_instance_state'])
        return dict_copy

