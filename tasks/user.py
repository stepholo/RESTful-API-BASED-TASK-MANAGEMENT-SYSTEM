#!/usr/bin/python3
"""Module to define class User"""


from tasks.base_task import TaskManager, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class User(TaskManager, Base):
    """Class to define the user who creates a task
        PUblic class attributes:
            first_name: string
            last_name: string
            email: string
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    tasks = relationship("Task", back_populates="user")

    def __init__(
            self,
            *args,
            first_name=None,
            last_name=None,
            email_address=None,
            **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if first_name is None:
            raise ValueError('What is your first name?')
        else:
            self.first_name = first_name

        if last_name is None:
            raise ValueError('What is your second name?')
        else:
            self.last_name = last_name

        if email_address is None:
            raise ValueError('What is your email address?')
        else:
            self.email_address = email_address
