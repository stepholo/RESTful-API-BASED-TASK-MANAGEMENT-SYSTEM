#!/usr/bin/python3
"""Module to test the console"""

from unittest.mock import patch
from io import StringIO
import os
import pytest
from tasks import storage
from tasks.users import User
from tasks.tasks import Task
from datetime import datetime, timedelta
from console import TASKCommand


@pytest.fixture
def task_command():
    return TASKCommand()


def test_preloop(capsys, task_command):
    task_command.preloop()
    captured = capsys.readouterr()
    assert "Welcome to Task Command interpreter" in captured.out


def test_emptyline(task_command):
    assert task_command.emptyline() is None


def test_do_clear_windows(mocker, task_command):
    mocker.patch("os.name", "nt")
    mocker.patch("os.system")

    task_command.do_clear(None)
    os.system.assert_called_once_with("cls")


def test_do_quit(task_command):
    assert task_command.do_quit(None) is True


def test_do_EOF(capsys, task_command):
    assert task_command.do_EOF(None) is True
    captured = capsys.readouterr()
    assert captured.out == "\n"


def test_do_create_user(capfd):
    task_command = TASKCommand()
    user_input = "create_user John Doe johndoe@example.com"

    with patch('builtins.input', return_value=user_input):
        task_command.onecmd(user_input)

    captured = capfd.readouterr()
    assert captured.out.strip() == "John Doe has been created"

    # Assert user creation
    created_user = storage.get_user_by_email(User, "johndoe@example.com")
    assert created_user.first_name == "John"
    assert created_user.last_name == "Doe"
    assert created_user.email_address == "johndoe@example.com"


def test_do_create_task(capfd):
    task_command = TASKCommand()
    user_input = "create_task johndoe@example.com " \
            "Code study_my_books high done 0"

    with patch('builtins.input', return_value=user_input):
        task_command.onecmd(user_input)

    captured = capfd.readouterr()
    expected_output = '__class__ - Task'
    assert captured.out.strip() == expected_output


def test_do_update_task()
