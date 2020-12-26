
from bash import bash
import pytest

from lily_env.git import assert_is_git_ignored, assert_is_git_repository
from lily_env.exceptions import FileNotIgnoredError
from tests import BaseTestCase


class GitTestCase(BaseTestCase):

    #
    # ASSERT_IS_GIT_IGNORED
    #
    def test_assert_is_git_ignored__is_ignored(self):

        bash('git init')
        self.root_dir.join('.gitignore').write('file.txt\n')
        f = self.root_dir.join('file.txt')
        f.write('whatever')

        assert assert_is_git_ignored(str(f)) is True

    def test_assert_is_git_ignored__is_not_ignored(self):

        bash('git init')
        self.root_dir.join('.gitignore').write('')
        f = self.root_dir.join('file.txt').write('whatever')

        with pytest.raises(FileNotIgnoredError):
            assert_is_git_ignored(str(f))

    #
    # ASSERT_IS_GIT_REPOSITORY
    #
    def test_assert_is_git_repository__is_repository(self):

        bash('git init')

        assert assert_is_git_repository() is True

    def test_assert_is_git_repository__is_not_repository(self):

        assert assert_is_git_repository() is False
