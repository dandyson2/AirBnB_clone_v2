#!/usr/bin/python3
"""
Compress web static package and deploy to server
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.25.19.204', '54.157.159.85']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Deploy web files to server
    """
    if not exists(archive_path):
        return False

    timestamp = archive_path.split('/')[-1][:-4]

    try:
        put(archive_path, '/tmp/')
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C '
            '/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* '
            '/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/web_static_{}/ '
            '/data/web_static/current'.format(timestamp))
        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False
