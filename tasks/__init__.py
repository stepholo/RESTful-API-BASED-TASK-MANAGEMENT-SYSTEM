#!/usr/bin/python3
"""Package initializer containing
    unique FileStorage instance for the application
"""


from tasks.engine.task_storage import FileStorage

storage = FileStorage()
storage.reload()
