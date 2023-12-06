#!/usr/bin/python3
"""Module to define class User"""


from tasks.base_task import TaskManager, Base
from sqlalchemy import Column, String, event
from sqlalchemy.orm import relationship
from uuid import uuid4


class User(TaskManager, Base):
    """Class to define the user who creates a task
        PUblic class attributes:
            first_name: string
            last_name: string
            email: string
    """
    __tablename__ = 'users'

    id = Column(String(60), primary_key=True)
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
            self.first_name = first_name.title()

        if last_name is None:
            raise ValueError('What is your last name?')
        else:
            self.last_name = last_name.title()

        if email_address is None:
            raise ValueError('What is your email address?')
        else:
            self.email_address = email_address

        if kwargs.get("id", None) is None:
            self.id = str(uuid4())

    def update_email_address(self, new_email):
        """Update the user's email address"""
        self.email_address = new_email
        self.save()


@event.listens_for(User.email_address, 'set')
def on_email_address_changed(target, value, oldvalue, initiator):
    """Update the associated tasks' email address when a
        user's email is changed
    """
    from tasks import storage
    from tasks.tasks import Task
    tasks = storage.all(Task)
    for task in tasks:
        if task.user_id == target.id:
            task.email_address = value
            task.save()
