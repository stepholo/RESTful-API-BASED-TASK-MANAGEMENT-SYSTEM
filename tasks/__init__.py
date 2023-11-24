#!/usr/bin/python3
"""Package initializer containing
    unique DBStorage instance for the application
"""


from tasks.engine.task_storage import DBStorage

storage = DBStorage()
storage.reload()
