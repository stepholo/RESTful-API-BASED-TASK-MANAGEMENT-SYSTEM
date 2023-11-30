#!/usr/bin/python3
"""Module that define class DBStorage"""


from tasks.base_task import Base
from tasks.tasks import Task
from tasks.users import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


storage = 'mysql'
user = 'root'
passwd = 'qw12ERty'
host = 'localhost'
db = 'tasks_db'

classes = {'User': User, 'Task': Task}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('{}://{}:{}@{}/{}'.format(
            storage, user, passwd, host, db
        ))
        self.reload()

    def all(self, cls=None):
        """query on the current database session"""
        if cls:
            return self.__session.query(cls).all()
        else:
            users = self.__session.query(User).all()
            task = self.__session.query(Task).all()
            return users, task

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
        self.save()

    def save(self, obj=None):
        """commit all changes of the current database session"""
        if obj is not None and isinstance(obj, User):
            users = self.all(User)
            if users:
                for user in users:
                    if user.email_address == obj.email_address:
                        raise ValueError('That email address has been taken')
        else:
            try:
                self.__session.commit()
            except Exception as e:
                self.__session.rollback()
                raise e

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj and isinstance(obj, User):
            self.__session.delete(obj)
            self.save()
            self.__session.query(Task).filter(Task.user_id == None).delete()
            self.save()
        elif obj and isinstance(obj, Task):
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def get_user_by_id(self, cls, id=None):
        """Returns the user object based on the class name and its ID, or
            None if not found
        """
        if cls not in classes.values():
            return None
        if cls == User and id is not None:
            value = self.__session.query(cls).filter_by(
                id=id).all()
            return value
        return None

    def get_user_by_email(self, cls, email=None):
        """Method to get user object by email address"""
        if cls not in classes.values() or email is None:
            return None
        user = self.__session.query(cls).filter_by(email_address=email).first()
        if user:
            return user
        else:
            raise ValueError('No user with such email')

    def get_task(self, cls, task_id=None, user_id=None, email=None):
        """Returns all task by task_id or user_id"""
        if cls not in classes.values():
            return None
        if cls == Task and task_id is not None:
            value = self.__session.query(cls).filter_by(
                task_id=task_id).first()
            return value
        if cls == Task and user_id is not None:
            value = self.__session.query(cls).filter_by(
                user_id=user_id).first()
            return value
        if cls == Task and email is not None:
            value = self.__session.query(cls).filter_by(
                email_address=email).all()
            return value
        return None
