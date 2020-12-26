
from bash import bash

from .exceptions import FileNotIgnoredError


def assert_is_git_ignored(filepath):
    result = bash(f'git check-ignore {filepath}')

    if result.stdout:
        return True

    else:
        raise FileNotIgnoredError


def assert_is_git_repository():
    result = bash('ls .git')

    if result.stderr:
        return False

    return True
