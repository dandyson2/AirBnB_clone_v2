#!/usr/bin/python3
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['100.25.19.204', '54.157.159.85']


def create_archive():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = "web_static_{}{}{}{}{}{}.tgz".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    file_path = os.path.join("versions", file_name)
    local("mkdir -p versions")
    local("tar -cvzf {} web_static".format(file_path))
    return file_path


def distribute_archive(archive_path):
    """Distributes an archive to a web server."""
    if os.path.isfile(archive_path):
        file_name = os.path.basename(archive_path)
        name = file_name.split(".")[0]
        remote_tmp_path = "/tmp/{}".format(file_name)
        remote_release_path = "/data/web_static/releases/{}/".format(name)

        put(archive_path, remote_tmp_path)
        run("mkdir -p {}".format(remote_release_path))
        run("tar -xzf {} -C {}".format(remote_tmp_path, remote_release_path))
        run("rm {}".format(remote_tmp_path))
        run("mv {}web_static/* {}".format(remote_release_path, remote_release_path))
        run("rm -rf {}web_static".format(remote_release_path))
        current_path = "/data/web_static/current"
        run("rm -rf {}".format(current_path))
        run("ln -s {} {}".format(remote_release_path, current_path))
        return True
    return False


def deploy():
    """Create and distribute an archive to a web server."""
    archive_path = create_archive()
    if archive_path:
        return distribute_archive(archive_path)
    return False
