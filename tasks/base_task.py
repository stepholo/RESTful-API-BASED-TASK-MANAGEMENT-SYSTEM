#!/usr/bin/python3
"""Module to define the base class TaskManager
    that all child class will inherit from
"""


import tasks
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class TaskManager:
    """Parent class TaskManager that defines attributes and methods
        to be inherited by the child classes.
        Attributes and methods:
            created_at: the current date and time when the instance was created
            updated_at: the current date and time when the instance was updated
            __str__: String representation of the instance
            save: updated the attribute updated_at with the current datetime
            to_dict: method to return keys/values of __dict__ of the task
            instance.
    """
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """class construct"""

        if args:
            raise TypeError('Positional arguments is not accepted(*args)')

        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())

    def __str__(self):
        """Returns string representation of an instance in
            the format of [<class name>] (<self.id>) <self.__dict__>
        """
        obj_name = self.__class__.__name__
        return f"[{obj_name}] {self.__dict__}"

    def save(self):
        """Method to update the attribute updated_at with
            the current datetime
        """
        self.updated_at = datetime.utcnow()
        tasks.storage.new(self)
        tasks.storage.save()

    def to_dict(self):
        """Method to return keys/value of __dict__ of the class instance
        """
        obj_dict = self.__dict__.copy()
        if 'created_at' in obj_dict:
            obj_dict['created_at'] = obj_dict['created_at'].strftime(time)
        if 'updated_at' in obj_dict:
            obj_dict['updated_at'] = obj_dict['updated_at'].strftime(time)
        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict

    def delete(self):
        """delete the current instance from the storage"""
        tasks.storage.delete(self)
