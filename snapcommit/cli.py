import os
import stat
import sys

import click
from click import secho

import snapconfig
import gitops

OK = click.style(u'[\u2713]', bold=True, fg='green')
BAD = click.style(u'[\u203C]', bold=True, fg='red')
hook_path = '.git/hooks/post-commit'

def _is_enabled(post_commit_file):
    with open(hook_path, 'r') as f:
        contents = f.read()
        return 'snap-commit' in contents

def write_hook_file(hook_path):
    with open(hook_path, 'a') as f:
        f.write('\nsnap-commit-hook&\n')
    os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IEXEC)
    secho(u'{} snap-commit enabled'.format(OK))

def disable_hook(hook_path):
    with open(hook_path, 'r+') as f:
        contents = [line for line in f.read().split('\n') if line is not '']
        f.seek(0)
        snap_line = [idx for idx, _ in enumerate(contents) if 'snap-commit' in _]
        contents.pop(snap_line[0])
        f.write('\n'.join(contents))
        f.truncate()
        secho(u'{} snap-commit disabled'.format(OK))

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    ctx.obj = snapconfig.load_config()

@cli.command(help='List images in IMAGE_DIR')
@click.pass_context
def list(ctx):
    image_dir = ctx.obj['image_dir']
    try:
        secho('Listing images in {}'.format(image_dir))
        images = sorted(os.listdir(image_dir))
        for idx, image in enumerate(images):
            secho('{:03d}. {}'.format(idx + 1, image))
    except OSError, e:
        secho('{}: {}'.format(e.strerror, image_dir))
        sys.exit(1)

@cli.command(help='Open an image in the default viewer')
@click.argument('image_id', required=False, type=int)
@click.pass_context
def show(ctx, image_id=None):
    image_dir = ctx.obj['image_dir']
    if not image_id:
        click.launch(image_dir, locate=True)
        return
    images = sorted(os.listdir(image_dir))
    image = images[image_id -1]
    secho('Showing image {}'.format(image))
    click.launch(os.path.join(image_dir, image))

@cli.command(help='Enable snap-commit in the current repo')
def enable():
    if gitops.is_repo:
        if os.path.isfile(hook_path):
            if not _is_enabled(hook_path):
                write_hook_file(hook_path)
                sys.exit(0)
            else:
                secho(u'{} snap-commit is already enabled for this repo'.format(OK))
                sys.exit(0)
        else:
            write_hook_file(hook_path)
            sys.exit(0)
    else:
        secho(u'{} Error: Directory is not a git repository'.format(BAD))
        sys.exit(1)

@cli.command(help='Disable snap-commit in the current repo')
def disable():
    if gitops.is_repo:
        if os.path.isfile(hook_path):
            if _is_enabled(hook_path):
                disable_hook(hook_path)
                sys.exit(0)
            else:
                secho(u'{} snap-commit is not enabled for this repo'.format(OK))
                sys.exit(0)
        else:
            secho(u'{} no post-commit file found, snap-commit is not enabled'.format(OK))
            sys.exit(0)
    else:
        secho(u'{} Error: Directory is not a git repository'.format(BAD))
        sys.exit(1)

if __name__ == '__main__':
    cli()
