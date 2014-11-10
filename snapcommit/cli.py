import os
import stat

import click

import gitops


hook_path = '.git/hooks/post-commit'

def _is_enabled(post_commit_file):
    with open(hook_path, 'r') as f:
        contents = f.read()
        return 'snap-commit' in contents

def write_hook_file(hook_path):
    with open(hook_path, 'a') as f:
        f.write('\npython /home/k/git/snap-commit/snapcommit/hook.py\n')
    os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IEXEC)

def enable():
    if gitops.is_repo:
        if not _is_enabled(hook_path):
            write_hook_file(hook_path)
            print 'snap-commit enabled'
        else:
            print 'snap-commit is already enabled for this repo'

def disable_hook(hook_path):
    with open(hook_path, 'r+') as f:
        contents = [line for line in f.read().split('\n') if line is not '']
        f.seek(0)
        snap_line = [idx for idx, _ in enumerate(contents) if 'snap-commit' in _]
        contents.pop(snap_line[0])
        f.write('\n'.join(contents))
        f.truncate()
        print 'snap-commit disabled'

def disable():
    if gitops.is_repo:
        if os.path.isfile(hook_path):
            if _is_enabled(hook_path):
                disable_hook(hook_path)
            else:
                print 'snap-commit is not enabled for this repo'
        else:
            print 'no post-commit file found, snap-commit is not enabled'
