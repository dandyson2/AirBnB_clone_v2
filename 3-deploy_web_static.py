#!/usr/bin/python3
import os
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['100.25.19.204', '54.157.159.85']

def create_archive():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = "web_static_{}{}{}{}{}{}.tgz".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    file_path = os.path.join("versions", file_name)
    
    if not os.path.exists("versions"):
        os.makedirs("versions")
    
    local("tar -czvf {} web_static".format(file_path))
    return file_path

def distribute_archive(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    with cd('/tmp'):
        put(archive_path, file_name)
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
    
    return True

def deploy():
    """Create and distribute an archive to a web server."""
    archive_path = create_archive()
    if archive_path:
        return distribute_archive(archive_path)
    return False
