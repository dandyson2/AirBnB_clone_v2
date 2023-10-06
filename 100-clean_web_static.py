#!/usr/bin/python3
import os
from fabric.api import env, lcd, cd, local, run

env.hosts = ['100.25.19.204', '54.157.159.85']

def do_clean(number=1):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.
    """
    number = int(number)
    number = max(number, 1)  # Ensure number is at least 1

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        archives_to_delete = local_archives[:-number]
        for archive in archives_to_delete:
            local(f"rm ./versions/{archive}")

    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        web_static_archives = [a for a in remote_archives if "web_static_" in a]
        archives_to_delete = web_static_archives[:-number]
        for archive in archives_to_delete:
            run(f"rm -rf ./data/web_static/releases/{archive}")
