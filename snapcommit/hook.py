import os
import json
from os import path

import requests

import gitops
import grab


def load_config(config_path=None):
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        defaults = [
            path.join(path.expanduser('~'), '.snap-commit.conf.json'),
            '/etc/snap-commit/snap-commit.conf.json',
            path.join(path.dirname(path.realpath(__file__)), 'defaults.json'),
        ]
        for config_path in defaults:
            if path.isfile(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    break
    if '~' in config['image_dir']:
        config['image_dir'] = config['image_dir'].replace(
            '~',
            path.expanduser('~')
        )
    return config

def new_path(prefix=None):
    commit = gitops.get_commit()
    remote = gitops.get_remote_url()
    if remote:
        host = remote.split('.')[0].split('@')[1]
        user, repo = remote.split(':')[1].replace('.git', '').split('/')
    else:
        host, user, repo = ['', '', '']
    filename = '{}_{}_{}_{}_{}.jpg'.format(
        commit.commit_time*1000,
        commit.hex[:7],
        user,
        repo,
        host
    )
    if prefix:
        paths = [prefix, filename]
    else:
        paths = [filename]
    return path.join(*paths)

def upload(config):
    base = config['image_dir']
    for item in os.listdir(base):
        try:
            filepath = path.join(base, item)
            r = requests.post(
                config['snap_server'] + '/v1',
                files={'file': (item, open(filepath, 'rb'))}
            )
            if r.ok:
                os.remove(filepath)
            else:
                print 'error occurred', r.status_code, r.text
        except requests.exceptions.RequestException, e:
            print 'error occurred', e
            print 'saving image for next upload'

def run_hook(config):
    file_path = new_path(config['image_dir'])
    try:
        os.makedirs(path.dirname(file_path))
    except OSError, e:
        if e.errno is not 17:
            raise
    grab.grab_image(
        file_path,
        width=config['width'],
        height=config['height'],
        device=config['video_device']
    )

def main():
    import sys
    if len(sys.argv) > 1:
        config = load_config(sys.argv[1])
    else:
        config = load_config()
    run_hook(config)
    if config.get('snap_server') and config['snap_server']:
        upload(config)
    sys.exit(0)


if __name__ == '__main__':
    main()
