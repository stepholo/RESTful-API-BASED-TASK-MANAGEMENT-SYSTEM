#!/usr/bin/python3
"""Module to define the base class TaskManager
    that all child class will inherit from
"""


import uuid
from datetime import datetime


class TaskManager:
    """Parent class TaskManager that defines attributes and methods
        to be inherited by the child classes.
        Attributes and methods:
            id: task instance assigned by random uuid (uuid4())
            created_at: the current date and time when the instance was created
            updated_at: the current date and time when the instance was updated
            __str__: String representation of the instance
            save: updated the attribute updated_at with the current datetime
            to_dict: method to return keys/values of __dict__ of the task
            instance.
    """
    def __init__(self, *args, **kwargs):
        """class construct"""

        if args:
            raise TypeError('Positional arguments is not accepted(*args)')
        elif kwargs:
            for key, value in kwargs.items():
                if key == 'id':
                    self.id = value
                elif key == 'created_at' or 'updated_at':
                    frmt = '%Y-%m-%dT%H:%M:%S.%f'
                    setattr(self, key, datetime.strptime(value, frmt))
                elif key == '__class__':
                    pass
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns string representation of an instance in
            the format of [<class name>] (<self.id>) <self.__dict__>
        """
        obj_name = self.__class__.__name__
        obj_id = self.id
        return f"[{obj_name}] ({obj_id}) {self.__dict__}"

    def to_dict(self):
        """Method to return keys/value of __dict__ of the class instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__
        obj_dict['created_at'] = obj_dict["created_at"].isoformat()
        obj_dict['updated_at'] = obj_dict["updated_at"].isoformat()
        return obj_dict
