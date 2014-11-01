import pygit2


REPO = pygit2.Repository('.git')

def get_commit():
    return REPO.revparse_single('HEAD')

def get_remote_url():
    for remote in REPO.remotes:
        return remote.url
