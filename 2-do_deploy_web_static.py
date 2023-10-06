#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import *
from os import path

env.hosts = ['<100.24.238.68>', '<34.224.3.204>']
env.user = '<ubuntu>'


def do_deploy(archive_path):
    if not path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        no_ext_name = archive_name.split('.')[0]
        remote_tmp_path = '/tmp/{}'.format(archive_name)
        remote_release_path = '/data/web_static/releases/{}/'.format(no_ext_name)

        # Upload archive
        put(archive_path, remote_tmp_path)

        # Uncompress archive
        run('mkdir -p {}'.format(remote_release_path))
        run('tar -xzf {} -C {}'.format(remote_tmp_path, remote_release_path))
        run('rm {}'.format(remote_tmp_path))

        # Delete old symbolic link, create new one
        run('rm -f /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(remote_release_path))

        return True

    except Exception as e:
        print(e)
        return False
