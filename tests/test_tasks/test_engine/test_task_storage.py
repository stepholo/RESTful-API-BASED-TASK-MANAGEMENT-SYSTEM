#!/usr/bin/python3
"""Pytest for the DBStorage class"""

import pytest
from unittest.mock import Mock
from tasks.engine.task_storage import DBStorage
from tasks.create_task import Task
from tasks.user import User


@pytest.fixture
def db_storage():
    """Fixture to create an instance of DBStorage"""
    return DBStorage()


def test_db_storage_initialization(db_storage):
    """Test DBStorage initialization"""
    assert db_storage.__engine is not None
    assert db_storage.__session is not None


def test_db_storage_all(db_storage):
    """Test the 'all' method in DBStorage"""
    # Create some mock data
    mock_user = Mock(spec=User)
    mock_task = Mock(spec=Task)

    # Add mock data to the database
    db_storage.new(mock_user)
    db_storage.new(mock_task)

    # Retrieve all users and tasks
    users, tasks = db_storage.all()

    # Check if the returned data contains the mock objects
    assert mock_user in users
    assert mock_task in tasks


def test_db_storage_new(db_storage):
    """Test the 'new' method in DBStorage"""
    # Create a mock user object
    mock_user = Mock(spec=User)

    # Add the mock user to the database
    db_storage.new(mock_user)

    # Retrieve all users and check if the mock user is present
    users, _ = db_storage.all(User)
    assert mock_user in users


if __name__ == "__main__":
    pytest.main()
