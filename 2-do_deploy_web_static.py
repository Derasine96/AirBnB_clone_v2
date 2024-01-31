#!/usr/bin/python3
""" a Fabric script that distributes an archive to your web servers"""
from fabric.api import *
import os

env.hosts = ['100.24.240.5', '100.25.33.28']

def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive_name = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(archive_name)[0]
        run("mkdir -p /data/web_static/releases/{}/".format(name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_name, name_no_ext))
        run("rm /tmp/{}".format(archive_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name_no_ext))
        return True
    except Exception as e:
        return False
