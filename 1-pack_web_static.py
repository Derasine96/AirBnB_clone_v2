#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of
        the web_static folder.
    """
    # create the versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.mkdir("versions")

    # generate the .tgz archive
    now = datetime.now()
    tar_fil = "versions/web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
    try:
        local("tar -cvzf {} web_static".format(tar_fil))
        print("web_static packed: {} -> {}Bytes"
              .format(tar_fil, os.path.getsize(tar_fil)))
        return tar_fil
    except Exception as e:
        return None
