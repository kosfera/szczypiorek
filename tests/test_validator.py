
from unittest import TestCase

from lily_env.validator import url, length, ValidatorError


class UrlTestCase(TestCase):

    def test_success(self):
        assert url('http://hi.io') is True

    def test_not_valid(self):

        try:
            url('hi.io')

        except ValidatorError as e:
            assert e.args[0] == 'Text "hi.io" is not valid URL'

        else:
            raise AssertionError('should raise error')


class LengthTestCase(TestCase):

    def test_success(self):
        assert length('hello world') is True

    def test_not_valid(self):

        try:
            length('hello', min_length=10)

        except ValidatorError as e:
            assert e.args[0] == 'Text "hello" is too short. min length: 10'

        else:
            raise AssertionError('should raise error')
