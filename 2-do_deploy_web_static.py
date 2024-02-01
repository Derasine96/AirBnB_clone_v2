#!/usr/bin/python3
"""A Fabric script that distributes an archive to your web servers"""
from fabric.api import *
import os

env.hosts = ['100.24.240.5', '100.25.33.28']
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
        run("rm -rf /data/web_static/current")

        cmd_link = ("ln -s /data/web_static/releases/{}/ "
                    "/data/web_static/current").format(name_no_ext)
        run(cmd_link)

        print("Deployment successful.")
        return True
    except Exception as e:
        print("Error during deployment:", str(e))
        return False
