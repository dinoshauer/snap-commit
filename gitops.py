import pygit2


REPO = pygit2.Repository('.git')

def get_commit():
    return REPO.revparse_single('HEAD')
    # rev.hex[:7], rev.commit_time*1000

def get_remote_url():
    for remote in REPO.remotes:
        if 'github' in remote.url:
            return remote.url
            # .split(':')[1].replace('.git', '').split('/')
