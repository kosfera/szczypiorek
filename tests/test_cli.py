
import os
from unittest import TestCase
import textwrap

from click.testing import CliRunner

import lily_env as env
from lily_env.cli import cli


class CliTestCase(TestCase):

    def setUp(self):
        self.runner = CliRunner()

    #
    # DUMP
    #
    def test_dump(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField()

            is_important = env.BooleanField()

            aws_url = env.URLField()

            number_of_workers = env.IntegerField()

        os.environ['SECRET_KEY'] = 'secret.whatever'
        os.environ['IS_IMPORTANT'] = 'true'
        os.environ['AWS_URL'] = 'http://hello.word.org'
        os.environ['NUMBER_OF_WORKERS'] = '113'

        MyEnvParser().parse()

        result = self.runner.invoke(cli, ['dump'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            AWS_URL: http://hello.word.org
            IS_IMPORTANT: True
            NUMBER_OF_WORKERS: 113
            SECRET_KEY: secret.whatever
        ''').strip()

    def test_dump__dump_was_not_created(self):
        pass
