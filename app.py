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

def upload():
    base = '/home/k/.snap-commit'
    for item in os.listdir(base):
        try:
            filepath = os.path.join(base, item)
            r = requests.post(
                'http://0.0.0.0:8000/v1/snaps',
                data=open(filepath, 'rb'),
            )
            if r.ok:
                os.remove(filepath)
            else:
                print 'error occurred', r.status_code, r.text
        except requests.exceptions.RequestException, e:
            print 'error occurred', e
            print 'saving image for next upload'

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
