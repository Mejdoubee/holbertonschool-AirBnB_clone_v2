#!/usr/bin/python3
'''
Model defines file_storage class that serializes instances
to a JSON file and deserializes JSON file to instances
'''
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    '''
    Serializes instances to a JSON file and deserializes JSON file to instances
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
        Returns the dictionary __objects
        If cls is provided, returns a filtered dictionary
        '''
        if not cls:
            return self.__objects
        else:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        '''
        Sets in __objects the obj with key <obj class name>.id
        '''
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        '''
        Serializes __objects to the JSON file
        '''
        with open(self.__file_path, 'w') as f:
            json.dump(
                {key: obj.to_dict() for key, obj in self.__objects.items()}, f)

    def reload(self):
        '''
        Deserializes the JSON file to __objects
        '''
        class_mapping = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
        }

        try:
            with open(FileStorage.__file_path) as file:
                obj_dict = json.load(file)

            for value in obj_dict.values():
                class_name = value.pop("__class__", None)
                if class_name:
                    class_instance = class_mapping.get(class_name)
                    if class_instance:
                        obj = class_instance(**value)
                        self.new(obj)

        except (FileNotFoundError, json.JSONDecodeError):
            return

    def delete(self, obj=None):
        '''
        delete obj from __objects if it’s inside - if obj is equal to None
        the method should not do anything
        '''
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    @property
    def reviews(self):
        """Return the list of Review instances with place_id equal to the current Place.id"""
        from models import storage
        all_reviews = storage.all(Review)
        place_reviews = [review for review in all_reviews.values() if review.place_id == self.id]
        return place_reviews

    def close(self):
        """ Deserializes the JSON file to objects """
        self.reload()