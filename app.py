import os
import json

import requests

import gitops
import grab


def new_path(prefix=None):
    commit = gitops.get_commit()
    user, repo = gitops.get_remote_url().split(':')[1].replace('.git', '').split('/')
    filename = '{}_{}_{}_{}.jpg'.format(
        commit.commit_time*1000,
        commit.hex[:7],
        user,
        repo
    )
    if prefix:
        paths = [prefix, filename]
    else:
        paths = [filename]
    return os.path.join(*paths)

def run_hook():
    path = new_path('/home/k/.snap-commit')
    try:
        os.makedirs(os.path.dirname(path))
    except OSError, e:
        if e.errno is not 17:
            raise
    grab.grab_image(path)


if __name__ == '__main__':
    import sys
    run_hook()
    sys.exit(0)
