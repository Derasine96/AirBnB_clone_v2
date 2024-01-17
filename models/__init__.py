#!/usr/bin/python3
"""Add a conditional depending of the value
     of the env variable HBNB_TYPE_STORAGE
"""
from os import getenv


storage_type = getenv('HBNB_TYPE_STORAGE')
if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
