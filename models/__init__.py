#!/usr/bin/python3
"""Add a conditional depending of the value
     of the env variable HBNB_TYPE_STORAGE
"""
import os
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


storage_type = os.environ.get('HBNB_TYPE_STORAGE', 'db')
if storage_type == 'db':
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
