#!/usr/bin/python3
"""API for Task"""

from tasks.tasks import Task
from tasks.users import User
from tasks import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from datetime import datetime, timedelta


@app_views.route('/tasks', methods=['GET'], strict_slashes=False)
def list_tasks():
    """Retrives the list of all Task objects"""
    tasks = storage.all(Task)
    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    return jsonify(task_list)


@app_views.route('/tasks/by_id/<id>', methods=['GET'], strict_slashes=False)
def get_task_id(id):
    """Get tasks by id"""
    tasks = storage.get_task(Task, task_id=id)
    if not tasks:
        abort(404)

    return jsonify(tasks.to_dict())


@app_views.route('/tasks/<email_address>',
                 methods=['GET'], strict_slashes=False)
def get_task_email(email_address):
    """Get tasks by user's email address"""
    tasks = storage.get_task(Task, email=email_address)
    if not tasks:
        abort(404)

    return jsonify([task.to_dict() for task in tasks])


@app_views.route('/user/tasks/<email_address>',
                 methods=['GET'], strict_slashes=False)
def get_user_task_email(email_address):
    """Get a user and all tasks related to it"""
    tasks = storage.get_task(Task, email=email_address)
    if not tasks:
        abort(404)

    users = storage.get_user_by_email(User, email=email_address)
    if not users:
        abort(404)

    return jsonify(users.to_dict(), [task.to_dict() for task in tasks])


@app_views.route('/tasks/<task_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_task(task_id):
    """Deletes task"""
    tasks = storage.get_task(Task, task_id=task_id)
    if not tasks:
        abort(404)

    storage.delete(tasks)
    return make_response(jsonify({}), 200)


@app_views.route('/tasks/<task_id>',
                 methods=['PUT'], strict_slashes=False)
def update_task(task_id):
    """Update a task"""
    task = storage.get_task(Task, task_id=task_id)
    if not task:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'completion_status' in data:
        completion_status = data['completion_status']
        if completion_status.lower() == 'done':
            task.deadline = datetime.now()
            task.days_to_complete = 0

    if 'days_to_complete' in data:
        days_to_complete = data['days_to_complete']
        if days_to_complete:
            days = int(days_to_complete)
            if days < 1:
                task.deadline = datetime.now()
            else:
                task.deadline = datetime.now() + timedelta(days=days)

    ignore = ['__class__', 'task_id', 'created_at',
              'updated_at' 'user_id' 'deadline']

    for key, value in data.items():
        if key not in ignore:
            setattr(task, key, value)

    storage.save()
    task = storage.get_task(Task, task_id=task_id)
    return make_response(jsonify(task.to_dict()), 200)


@app_views.route('/tasks/<email_address>',
                 methods=['POST'], strict_slashes=False)
def create_task(email_address):
    """Create a task based on existing user's email address"""
    if not request.get_json():
        abort(404, description='Not a JSON')

    if 'completion_status' not in request.get_json():
        abort(400, description="What is the work status (pending, done)")
    if 'days_to_complete' not in request.get_json():
        abort(400, description="Missing number of days to complete task")
    if 'description' not in request.get_json():
        abort(400, description='Missing task description')
    if 'priority_level' not in request.get_json():
        abort(400, description='Missing task priority level (high, low, medium)')
    if 'title' not in request.get_json():
        abort(400, description='Missing task title')

    data = request.get_json()
    data['email_address'] = email_address
    task = Task(**data)
    task.title = data['title']
    task.description = data['description']
    task.days_to_complete = data['days_to_complete']
    task.save()
    return make_response(jsonify(task.to_dict()), 201)
