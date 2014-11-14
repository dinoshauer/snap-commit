from os import path


DEFAULTS = {
    'image_dir': '~/.snap-commits/snaps/',
    'video_device': '/dev/video0',
    'width': 640,
    'height': 480,
    'snap_server': 'http://0.0.0.0:5000',
    'log_dir': '~/.snap-commits/logs/',
    'log_level': 'info',
    'keep_snaps': False
}

def load_config(config_path=None):
    config = {}
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
    config = dict(DEFAULTS.items() + config.items())
    if '~' in config['image_dir']:
        config['image_dir'] = config['image_dir'].replace(
            '~',
            path.expanduser('~')
        )
    return config
