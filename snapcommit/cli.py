import os
import stat
import sys

import click
from click import secho

import snapconfig
import gitops


hook_path = '.git/hooks/post-commit'

def _is_enabled(post_commit_file):
    with open(hook_path, 'r') as f:
        contents = f.read()
        return 'snap-commit' in contents

def write_hook_file(hook_path):
    with open(hook_path, 'a') as f:
        f.write('\nsnap-commit-hook&\n')
    os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IEXEC)
    secho('snap-commit enabled')

def disable_hook(hook_path):
    with open(hook_path, 'r+') as f:
        contents = [line for line in f.read().split('\n') if line is not '']
        f.seek(0)
        snap_line = [idx for idx, _ in enumerate(contents) if 'snap-commit' in _]
        contents.pop(snap_line[0])
        f.write('\n'.join(contents))
        f.truncate()
        secho('snap-commit disabled')

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    ctx.obj = snapconfig.load_config()

@cli.command()
@click.pass_context
def list(ctx):
    image_dir = ctx.obj['image_dir']
    try:
        secho('Listing images in {}'.format(image_dir))
        for idx, image in enumerate(os.listdir(image_dir)):
            secho('{:03d}. {}'.format(idx + 1, image))
    except OSError, e:
        secho('{}: {}'.format(e.strerror, image_dir))

@cli.command()
def enable():
    if gitops.is_repo:
        if os.path.isfile(hook_path):
            if not _is_enabled(hook_path):
                write_hook_file(hook_path)
                sys.exit(0)
            else:
                secho('snap-commit is already enabled for this repo')
                sys.exit(0)
        else:
            write_hook_file(hook_path)
            sys.exit(0)
    else:
        secho('Error: Directory is not a git repository')
        sys.exit(1)

@cli.command()
def disable():
    if gitops.is_repo:
        if os.path.isfile(hook_path):
            if _is_enabled(hook_path):
                disable_hook(hook_path)
                sys.exit(0)
            else:
                secho('snap-commit is not enabled for this repo')
                sys.exit(0)
        else:
            secho('no post-commit file found, snap-commit is not enabled')
            sys.exit(0)
    else:
        secho('Error: Directory is not a git repository')
        sys.exit(1)

if __name__ == '__main__':
    cli()
