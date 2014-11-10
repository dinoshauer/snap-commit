import pygit2


try:
    REPO = pygit2.Repository('.git')
    is_repo = True
except KeyError:
    is_repo = False


def get_commit():
    return REPO.revparse_single('HEAD')

def get_remote_url():
    for remote in REPO.remotes:
        return remote.url
