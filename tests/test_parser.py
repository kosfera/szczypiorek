
import textwrap

import pytest

import lily_env as env
from lily_env.parser import Env
from lily_env.exceptions import ValidatorError
from lily_env.crypto import encrypt
from tests import BaseTestCase


class EnvTestCase(BaseTestCase):

    #
    # __INIT__
    #
    def test__init__(self):

        e = Env(is_prod=True, secret_key='hello')

        assert e.is_prod is True
        assert e.secret_key == 'hello'


class EnvParserTestCase(BaseTestCase):

    def test_parse(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField()

            is_important = env.BooleanField()

            aws_url = env.URLField()

            number_of_workers = env.IntegerField()

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: http://hello.word.org

            number:
              of:
                workers: '113'
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        e = MyEnvParser().parse()

        assert e.secret_key == 'secret.whatever'
        assert e.is_important is True
        assert e.aws_url == 'http://hello.word.org'
        assert e.number_of_workers == 113

    def test_parse__complex_example(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField()

            is_important = env.BooleanField()

            aws_url = env.URLField()

            number_of_workers = env.IntegerField()

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: {{ a.b.c }}

            number:
              of:
                workers: '113'
            a:
              b:
                c: http://hello.word.org
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        e = MyEnvParser().parse()

        assert e.secret_key == 'secret.whatever'
        assert e.is_important is True
        assert e.aws_url == 'http://hello.word.org'
        assert e.number_of_workers == 113

    def test_parse__optional_with_defaults(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField(required=False, default='hello')

            is_important = env.BooleanField(required=False, default=False)

            aws_url = env.URLField(required=False, default='http://hi.pl')

            number_of_workers = env.IntegerField(required=False, default=12)

        content = encrypt(textwrap.dedent('''
            what:
              event: yo
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        e = MyEnvParser().parse()

        assert e.secret_key == 'hello'
        assert e.is_important is False
        assert e.aws_url == 'http://hi.pl'
        assert e.number_of_workers == 12

    def test_parse__optional_without_defaults(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField(required=False, allow_null=True)

            is_important = env.BooleanField(required=False, allow_null=True)

            aws_url = env.URLField(required=False, allow_null=True)

            number_of_workers = env.IntegerField(
                required=False, allow_null=True)

        content = encrypt(textwrap.dedent('''
            what:
              event: yo
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        e = MyEnvParser().parse()

        assert e.secret_key is None
        assert e.is_important is None
        assert e.aws_url is None
        assert e.number_of_workers is None

    def test_parse__validation_errors(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField(max_length=12)

            is_important = env.BooleanField()

            aws_url = env.URLField()

            number_of_workers = env.IntegerField()

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: whatever
            aws:
              url: not.url

            number:
              of:
                workers: not.number
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        with pytest.raises(ValidatorError) as e:
            MyEnvParser().parse()

        assert e.value.args[0] == (
            'env.aws_url: Text "not.url" is not valid URL')
