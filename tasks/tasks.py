#!/usr/bin/python3
"""Module that defines class CreateTask and inherits from TaskManager class"""


from tasks.base_task import TaskManager, Base
from tasks.users import User
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Task(TaskManager, Base):
    """Class CreateTask inherits from TaskManager
        Public class attributes:
            task_id: must be an int
            email_address: user email who creates the task
            created_at: datetime
            priority level: empty string
            Status: must be string
            Description: must be string
            days_to_complete: number of days remaining complete the task
            completion_status: whether the task has been done or pending
            deadline: datetime when the task should be completely done
    """
    __tablename__ = 'tasks'

    user_id = Column(Integer, ForeignKey('users.id'))
    email_address = Column(String(100), nullable=False)
    task_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    priority_level = Column(String(100), nullable=False)
    completion_status = Column(String(60), nullable=False)
    deadline = Column(DateTime)
    days_to_complete = Column(Integer, nullable=True)

    user = relationship('User', back_populates="tasks")

    PRIORITY_LEVELS = ['high', 'medium', 'low']
    COMPLETION_STATUS = ['pending', 'done']

    def __init__(self,
                 *args,
                 days_to_complete=None,
                 priority_level=None,
                 completion_status=None,
                 email_address=None,
                 **kwargs):
        """initialize Task class"""
        super().__init__(*args, **kwargs)

        if days_to_complete is not None:
            self.deadline = datetime.now() + timedelta(days=days_to_complete)

        if priority_level:
            self.priority_level = self._validate_priority(
                priority_level).lower()

        if completion_status:
            self.completion_status = self._validate_completion_status(
                completion_status).lower()

        if email_address is None:
            raise ValueError('User email is required to create task')
        user_id, email_address = self._auto_update_user_id(email_address)
        self.user_id = user_id
        self.email_address = email_address

    def _validate_priority(self, priority):
        """Validate and set priority level"""
        if priority not in self.PRIORITY_LEVELS:
            raise ValueError(
                f'Allowed priority: {". ".join(self.PRIORITY_LEVELS)}')
        return priority

    def _validate_completion_status(self, status):
        """Validate and set completion status"""
        if status not in self.COMPLETION_STATUS:
            raise ValueError(
                f'Allowed status: {", ".join(self.COMPLETION_STATUS)}')
        return status

    def _auto_update_user_id(self, user_email):
        """Used to auto update the user_id"""
        from tasks import storage
        user = storage.get_user_by_email(User, email=user_email)
        if user:
            return user.id, user.email_address
        else:
            raise ValueError(f'No user found with email {user_email}')
