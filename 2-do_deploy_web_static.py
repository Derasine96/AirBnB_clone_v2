#!/usr/bin/python3
"""A Fabric script that distributes an archive to your web servers"""
from fabric.api import *
import os

env.hosts = ['18.209.224.207', '54.237.19.209']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        print("Error: Archive path does not exist.")
        return False

    try:
        archive_name = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(archive_name)[0]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(name_no_ext))

        cmd_extr = "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_name, name_no_ext)
        run(cmd_extr)

        run("rm /tmp/{}".format(archive_name))
        cmd_move = ("mv /data/web_static/releases/{0}/web_static/* "
                    "/data/web_static/releases/{0}/").format(name_no_ext)
        run(cmd_move)

        cmd_remove_inner = ("rm -rf /data/web_static/releases/{}/web_static"
                            .format(name_no_ext))
        run(cmd_remove_inner)
        run("rm -rf /data/web_static/current")

        cmd_link = ("ln -s /data/web_static/releases/{}/ "
                    "/data/web_static/current").format(name_no_ext)
        run(cmd_link)

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error during deployment:", str(e))
        return False
