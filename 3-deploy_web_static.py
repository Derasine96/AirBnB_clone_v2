#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.24.240.5', '100.25.33.28']
env.user = "ubuntu"


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

        # Additional commands to move contents and remove inner folder
        cmd_move = ("mv /data/web_static/releases/{0}/web_static/* "
                    "/data/web_static/releases/{0}/").format(name_no_ext)
        run(cmd_move)

        cmd_remove_inner = ("rm -rf /data/web_static/releases/{}/web_static"
                            .format(name_no_ext))
        run(cmd_remove_inner)

        print("Deployment successful.")
        return True
    except Exception as e:
        print("Error during deployment:", str(e))
        return False


def deploy():
    """Calls do_pack and do_deploy, returns result of do_deploy"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
