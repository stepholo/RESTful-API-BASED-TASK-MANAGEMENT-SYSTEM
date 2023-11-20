#!/usr/bin/python3
"""Module to define the base class TaskManager
    that all child class will inherit from
"""


import uuid
from datetime import datetime
from tasks import storage


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
        mandatory_args = {'user_name', 'user_email'}
        missing_args = mandatory_args - set(kwargs.keys())

        if missing_args:
            raise ValueError(
                f"Missing mandatory arguments(s): {', '.join(missing_args)}")
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.user_name = kwargs['user_name']
        self.user_email = kwargs['user_email']
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())

    def __str__(self):
        """Returns string representation of an instance in
            the format of [<class name>] (<self.id>) <self.__dict__>
        """
        obj_name = self.__class__.__name__
        obj_id = self.id
        return f"[{obj_name}] ({obj_id}) {self.__dict__}"

    def save(self):
        """Method to update the attribute updated_at with
            the current datetime
        """
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Method to return keys/value of __dict__ of the class instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__
        obj_dict['created_at'] = obj_dict["created_at"].isoformat()
        obj_dict['updated_at'] = obj_dict["updated_at"].isoformat()
        return obj_dict
